from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SOSRequestViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('sos', SOSRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
