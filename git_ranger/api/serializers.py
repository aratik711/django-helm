from rest_framework import serializers
from .models import AccessTokenlist


class AccessTokenlistSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = AccessTokenlist
        fields = ('id', 'name', 'value', 'owner', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')

