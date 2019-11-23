from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Welcome

# Create your views here.
class HelloBroker(APIView):

    def get(self, request):
        return Response({"message": "Hello, Welcome Broker!"})
    