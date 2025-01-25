from rest_framework import generics
from rest_framework.response import Response
from userdata.permissions import AccessGroupPermission


class TestView(generics.GenericAPIView):
    permission_classes = (AccessGroupPermission,)
    access_level = "com.dept.team"  # change this to test permissions.

    def get(self, request):
        return Response("success", status=200)
