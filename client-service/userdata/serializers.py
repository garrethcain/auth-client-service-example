from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from .models import AccessGroup

User = get_user_model()


class AccessGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessGroup
        fields = ("access_level",)


class TokenUserSerializer(serializers.ModelSerializer):
    accessgroup = AccessGroupSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "email",
            "last_name",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "accessgroup",
        )

    def create(self, validated_data):
        """
        The `.update()` method does not support writable nested fields by default.
        Write an explicit `.update()` method for serializer `customuser.serializer.TokenUserSerializer`,
        or set `read_only=True` on nested serializer fields.
        """
        user_id = validated_data.pop(get_user_model().USERNAME_FIELD)
        accessgroup = validated_data.pop("accessgroup")
        user, _ = User.objects.get_or_create(email=user_id, defaults=validated_data)

        serializer = AccessGroupSerializer(data=accessgroup)
        created = serializer.is_valid(raise_exception=False)
        if not created:
            user.delete()  # remove to avoid integrity errors.
            raise exceptions.ParseError(
                "Integrity error, failed to parse the received payload through the serializer. "
                "Maybe data from a relationship is missing."
            )
        serializer.save(user=user)
        return user

    def update(self, instance, validated_data):
        accessgroup = validated_data.pop("accessgroup")
        # Confirm the relatioship exists.
        existing_accessgroup = (
            instance.accessgroup if hasattr(instance, "accessgroup") else None
        )
        serializer = AccessGroupSerializer(
            data=accessgroup, instance=existing_accessgroup
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=instance)

        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        # Do no update email, its a primary key.
        instance.last_login = validated_data["last_login"]
        instance.is_active = validated_data["is_active"]
        instance.is_staff = validated_data["is_staff"]
        instance.is_superuser = validated_data["is_superuser"]
        instance.save()
        return instance
