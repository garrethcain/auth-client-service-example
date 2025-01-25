from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AccessGroup(models.Model):
    """
    An example model adding some additional fields to the EasyJWT_User model via relationship.

    A contrived example of extra user data, add any extra fields required.
    """

    user = models.OneToOneField(
        User, related_name="accessgroup", on_delete=models.CASCADE
    )
    access_level = models.TextField(default="com.dept.team")
