from rest_framework import serializers

from src.customer.models import Profile, CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", required=False)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    bio = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    location = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'bio', 'image', 'location')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, min_length=8)

    def validate(self, data):
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        new_password_confirm = data.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                {"new_password_confirm": "Пароли не совпадают"}
            )

        user = self.context["request"].user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {"old_password": "Неверный пароль"}
            )
        if old_password == new_password:
            raise serializers.ValidationError(
                {"new_password": "Новый пароль должен отличаться от старого"}
            )
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user