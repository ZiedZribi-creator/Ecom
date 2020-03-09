from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import OrderViewset

router = routers.DefaultRouter()
router.register('order',OrderViewset)

urlpatterns = [
path('',include(router.urls)),

]
