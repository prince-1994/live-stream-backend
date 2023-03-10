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

from apps.checkout.views import CartItemViewSet, OrderItemViewSet, OrderViewSet
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from apps.channels.views import ChannelViewSet
from apps.products.views import CategoryViewSet, ProductViewSet
from apps.shows.views import ShowViewSet, StreamViewSet
from apps.profiles.views import AddressViewset
from apps.social.views import SocialViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import exchange_token

router = DefaultRouter()
router.register(r"channels", ChannelViewSet, basename="channel")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"shows", ShowViewSet, basename="show")
router.register(r"cart-items", CartItemViewSet, basename="cart")
router.register(r"addresses", AddressViewset, basename="address")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"order-items", OrderItemViewSet, basename="order-item")
router.register(r"streams", StreamViewSet, basename="stream")
router.register(r"socials", SocialViewSet, basename="social")

urlpatterns = []
urlpatterns += router.urls
urlpatterns += [
    path("chat/", include("apps.chats.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/social/<str:backend>/login/", exchange_token, name="social-auth"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
