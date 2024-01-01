from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from remotejwt_auth.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Example of how to add custom fields to the JWT.
    """

    username_field = get_user_model().USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        username_value = getattr(user, cls.username_field)
        token = super().get_token(user)

        # Example of custom field from custom model.
        try:
            token["field1"] = user.customuserfield.field1
        except ObjectDoesNotExist:
            pass

        token[cls.username_field] = username_value
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["is_superuser"] = user.is_superuser
        return token
