from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import CartViewset

router = routers.DefaultRouter()
router.register('cart',CartViewset)

urlpatterns = [
path('',include(router.urls)),

]
