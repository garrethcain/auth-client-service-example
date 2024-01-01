from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your models here.


class CustomUserField(models.Model):
    """
    An example model adding some additional fields to the RemoteJWT_User model via relationship.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field1 = models.CharField(max_length=32, default="field1 value")
    field2 = models.CharField(max_length=32, default="field2 value")
    field3 = models.CharField(max_length=32, default="field3 value")
