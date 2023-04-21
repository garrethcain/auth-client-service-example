from rest_framework import generics
from rest_framework.response import Response

class TestView(generics.GenericAPIView):
    def get(self, request):
        return Response("success", status=200)
