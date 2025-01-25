from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AccessGroup


User = get_user_model()


class AccessGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessGroup
        fields = (
            "access_level",
            # add any extra fields added
            # to the model here.
        )


class TokenUserSerializer(serializers.ModelSerializer):
    accessgroup = AccessGroupSerializer(allow_null=False)

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
