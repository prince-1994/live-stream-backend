"""shopbig URL Configuration

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

from apps.checkout.views import CartViewSet, OrderItemViewSet, OrderViewSet
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from apps.channels.views import ChannelViewSet
from apps.products.views import CategoryViewSet, ProductViewSet
from apps.shows.views import ShowViewSet, StreamViewSet
from apps.profiles.views import AddressViewset
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'channels', ChannelViewSet, basename='channel')
router.register(r'products', ProductViewSet, basename="product")
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'shows', ShowViewSet, basename='show')
router.register(r'cart-items', CartViewSet, basename='cart')
router.register(r'addresses', AddressViewset, basename='address')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'streams', StreamViewSet, basename='stream')

urlpatterns = []
urlpatterns += router.urls
urlpatterns += [
    path('chat/', include('apps.chats.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
