"""tslclone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.checkout.views import EditCartViewSet
from django.views.generic import base
from apps.shows.models import Show
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from apps.channels.views import ChannelViewSet, EditChannelViewSet, get_aws_channel, get_aws_stream_key, get_aws_stream
from apps.products.views import CategoryViewSet, ProductViewSet, EditProductViewSet
from apps.shows.views import ShowViewSet, EditShowViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'channels', ChannelViewSet, basename='channel')
router.register(r'products', ProductViewSet, basename="product")
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'shows', ShowViewSet, basename='show')
router.register(r'cart', EditCartViewSet, basename='cart')

channels_edit_router = DefaultRouter()
channels_edit_router.register(r'channels', EditChannelViewSet, basename='editchannel')

products_edit_router = DefaultRouter()
products_edit_router.register(r'products', EditProductViewSet, basename="editproduct")

shows_edit_router = DefaultRouter()
shows_edit_router.register(r'shows', EditShowViewSet, basename="editshow")
# router.register(r'videos', VideoViewSet, basename="video")

urlpatterns = []
urlpatterns += router.urls
urlpatterns += [
    path('chat/', include('apps.chats.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include(channels_edit_router.urls)),
    path('channels/<int:channel_id>/',include(products_edit_router.urls)),
    path('channels/<int:channel_id>/', include(shows_edit_router.urls)),
    path('channel-details/<int:channel_id>/', get_aws_channel),
    path('channel-details/<int:channel_id>/stream/', get_aws_stream),
    path('channel-details/<int:channel_id>/stream-key/', get_aws_stream_key),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
