from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class TileMetadataSerializer(serializers.Serializer):

    levels = serializers.IntegerField(
        help_text='Number of zoom levels in the image.',
        min_value=1,
        read_only=True,
    )
    size_x = serializers.IntegerField(
        help_text='Image size in the X direction.',
        min_value=1,
        read_only=True,
        source='sizeX',
    )
    size_y = serializers.IntegerField(
        help_text='Image size in the Y direction.',
        min_value=1,
        read_only=True,
        source='sizeY',
    )
    tile_size = serializers.IntegerField(
        help_text='Size of the square tiles the image is composed of.',
        min_value=1,
        read_only=True,
        source='tileSize',
    )
