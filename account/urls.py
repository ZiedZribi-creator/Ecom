from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from .views import UserViewSet,AdminProfileViewSet,ClientProfileViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('adminprofile', AdminProfileViewSet)
router.register('clientprofile', ClientProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('simple-profile/<slug:slug>/',SimpleProfileRetrieveView.as_view())

]
