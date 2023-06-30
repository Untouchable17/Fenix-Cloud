from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include

from src.customer import views

router = DefaultRouter()
router.register(r"profile", views.ProfileViewSet, basename="profile")
router.register(r"change_password", views.UserChangePasswordViewSet, basename="change_password")

urlpatterns = []
urlpatterns += router.urls
