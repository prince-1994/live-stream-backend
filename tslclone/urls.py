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
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import viewsets
from channels.views import ChannelViewSet, EditChannelViewSet
from products.views import ProductViewSet, EditProductViewSet, ProductImagesList
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'channels', ChannelViewSet, basename='channel')
router.register(r'products', ProductViewSet, basename="product")
router.register(r'users', viewsets.ViewSet, basename="user")

channels_edit_router = DefaultRouter()
channels_edit_router.register(r'channels', EditChannelViewSet, basename='editchannel')

products_edit_router = DefaultRouter()
products_edit_router.register(r'products', EditProductViewSet, basename="editproduct")

# router.register(r'videos', VideoViewSet, basename="video")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', include(channels_edit_router.urls)),
    path('channels/<int:channel_id>/',include(products_edit_router.urls))

]
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
