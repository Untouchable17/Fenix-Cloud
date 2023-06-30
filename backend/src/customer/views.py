from django.shortcuts import render

from rest_framework import status, viewsets, mixins, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from src.customer.models import Profile, CustomUser
from src.customer import serializers


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class UserChangePasswordViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been updated successfully."})
