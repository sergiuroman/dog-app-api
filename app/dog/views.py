from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Dog

from dog import serializers


class DogViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.DogSerializer
    queryset = Dog.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """retrieve the dogs for the authenticated user"""
        return self.queryset.order_by('-id')

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
