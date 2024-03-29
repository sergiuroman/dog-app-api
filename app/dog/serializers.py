from rest_framework import serializers

from core.models import Dog, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')
        read_only_fields = ('id',)


class DogSerializer(serializers.ModelSerializer):
    """serialize a dog"""

    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Dog
        fields = ('id', 'user', 'name', 'description',
                  'location', 'size', 'age', 'purpose', 'image', 'lat', 'long')
        read_only_fields = ('id',)


class DogImageSerializer(serializers.ModelSerializer):
    """serializer for uploading images to dogs"""

    class Meta:
        model = Dog
        fields = ('id', 'image')
        read_only_fields = ('id',)
