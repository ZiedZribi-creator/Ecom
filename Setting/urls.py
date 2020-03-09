from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import SocialMediaViewset


router = routers.DefaultRouter()
router.register('sm',SocialMediaViewset)


urlpatterns = [
        path('',include(router.urls)),

]
