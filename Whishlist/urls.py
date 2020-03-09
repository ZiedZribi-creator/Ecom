from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import WhishListViewset

router = routers.DefaultRouter()
router.register('whishlist',WhishListViewset)

urlpatterns = [
path('',include(router.urls)),

]
