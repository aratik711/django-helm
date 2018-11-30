from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import AccessTokenlistSerializer
from .models import AccessTokenlist



class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = AccessTokenlist.objects.all()
    serializer_class = AccessTokenlistSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new accesstokenlist."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Only return accesstokenlist items owned by the currently authenticated user."""
        return AccessTokenlist.objects.filter(owner=self.request.user)

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = AccessTokenlist.objects.all()
    serializer_class = AccessTokenlistSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)