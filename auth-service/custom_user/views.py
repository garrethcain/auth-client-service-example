from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model

from .serializers import TokenUserSerializer


User = get_user_model()

class TokenUserDetailView(generics.RetrieveAPIView):
    serializer_class = TokenUserSerializer

    def get_queryset(self):
        """
        Restrict the requesting user to only get what they
        have access too.
        """
        pk = self.kwargs.get("pk")
        user = self.request.user
        if any([user.is_staff, user.is_superuser]):
            return User.objects.filter(id=pk)
        # We should return an access error if trying to view a uer
        # that is not you, not a blind success.
        return User.objects.filter(id=user.id)
