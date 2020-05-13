from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from . import serializers
from . import models
from . import permissions

# Create your views here.

class HelloApiView(APIView):

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):

        an_apiview = [
            "Uses HTTP methods as function (get, post, patch, put, delete)",
            "It is similar to a traditional Django view",
            "Gives you the most control over your logic",
            "Is mapped manually to URLs"
        ]
        
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {}'.format(name)
            return Response({'message' : message})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        return Response({'method':'PATCH'}) # does not need to be method, can be message

    def put(self, request, pk=None):
        return Response({'method':'PUT'})

    def delete(self, request, pk=None):
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):

    serializer_class = serializers.HelloSerializer

    def list(self, request):

        return Response({'message':'Hello'})

    def create(self, request):

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {}'.format(name)
            return Response({'message' : message})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({'http_method':'GET'})

    def update(self, request, pk=None):
        return Response({'http_method':'PUT'})

    def partial_update(self, request, pk=None):
        return Response({'http_method':'PATCH'})

    def delete(self, request, pk=None):
        return Response({'http_method':'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all() #list all

    # add authentication
    authentication_class = (TokenAuthentication,)
    permissions_class = (permissions.UpdateOwnProfile,)

    # add filters
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    """ Checks email and password and returns an auth token """

    serializers_class = AuthTokenSerializer

    def create(self, request):
        """ Use an ObtainAuthToken to validate and create a token"""

        return ObtainAuthToken().post(request)