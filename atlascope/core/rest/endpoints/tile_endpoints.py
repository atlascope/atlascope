import io
from itertools import cycle

import PIL
from django.urls import path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from large_image.exceptions import TileSourceError
from large_image_source_ometiff import OMETiffFileTileSource
from large_image_source_tiff import TiffFileTileSource
import numpy
from rest_framework import mixins
from rest_framework.exceptions import APIException, NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response

from atlascope.core.models import Dataset
from atlascope.core.rest.additional_serializers import TileMetadataSerializer
from atlascope.core.utils.fuse import remote_dataset_to_local_path


class TileMetadataView(GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Dataset.objects.filter(content__isnull=False, dataset_type='tile_source')
    serializer_class = TileMetadataSerializer

    def get(self, *args, **kwargs):
        dataset = self.get_object()
        file_path = remote_dataset_to_local_path(dataset)
        try:
            tile_source = OMETiffFileTileSource(file_path)
        except TileSourceError:
            tile_source = TiffFileTileSource(file_path)
        serializer = self.get_serializer(tile_source)
        return Response(serializer.data)


class LargeImageRenderer(BaseRenderer):
    media_type = 'image/png'
    format = 'png'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class TileView(GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Dataset.objects.filter(content__isnull=False, dataset_type='tile_source')
    model = Dataset
    renderer_classes = [LargeImageRenderer]

    default_colors = ['#ffffff']

    @swagger_auto_schema(
        responses={200: 'Image file', 404: 'Image tile not found'},
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='A string identifying this dataset.',
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'z',
                openapi.IN_PATH,
                description=(
                    (
                        'The Z level of the tile. May range from [0, levels], where 0 '
                        'is the lowest resolution, single tile for the whole source.'
                    )
                ),
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'x',
                openapi.IN_PATH,
                description='The 0-based x position of the tile on the specified z level.',
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'y',
                openapi.IN_PATH,
                description='The 0-based y position of the tile on the specified z level.',
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, *args, x=None, y=None, z=None, **kwargs):
        dataset = self.get_object()
        file_path = remote_dataset_to_local_path(dataset)
        try:
            try:
                tile_source = OMETiffFileTileSource(file_path)
            except TileSourceError:
                tile_source = TiffFileTileSource(file_path)
            channels = self.request.query_params.get('channels')
            if channels:
                channels = channels.split(',')
            else:
                channels = range(len(tile_source.getMetadata()['frames']))
            colors = self.request.query_params.get('colors')
            if colors:
                colors = [f'#{color}' for color in colors.split(',')]
            else:
                colors = self.default_colors
            composite = None
            for channel, color in list(zip(channels, cycle(colors))):
                tile = tile_source.getTile(
                    x,
                    y,
                    z,
                    frame=channel,
                )
                tile_data = numpy.array(PIL.Image.open(io.BytesIO(tile)))
                if not composite:
                    composite = PIL.Image.new('RGBA', tile_data.shape, '#000000')
                mask_color = PIL.Image.new('RGBA', tile_data.shape, color)
                mask = PIL.Image.fromarray(tile_data)
                composite = PIL.Image.composite(mask_color, composite, mask)
            buf = io.BytesIO()
            composite.save(buf, format="PNG")
            return Response(buf.getvalue())
        except TileSourceError as e:
            error_msg = str(e)
            for missing_msg in (
                'z layer does not exist',
                'x is outside layer',
                'y is outside layer',
            ):
                if missing_msg in error_msg:
                    raise NotFound()
            raise APIException(error_msg)


urlpatterns = [
    path('datasets/<str:pk>/tiles/metadata', TileMetadataView.as_view()),
    path('datasets/<str:pk>/tiles/<int:z>/<int:x>/<int:y>.png', TileView.as_view()),
]
