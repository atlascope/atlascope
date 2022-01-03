from django.http.response import HttpResponse
from django.urls import path
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from large_image.exceptions import TileSourceError
from large_image_source_gdal import GDALFileTileSource
from rest_framework import mixins
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from atlascope.core.models import Dataset
from atlascope.core.rest.additional_serializers import TileMetadataSerializer


class TileMetadataView(GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Dataset.objects.filter(content__isnull=False, dataset_type='tile_source')
    permission_classes = [IsAuthenticated]
    serializer_class = TileMetadataSerializer

    def get(self, *args, **kwargs):
        dataset = self.get_object()
        tile_source = GDALFileTileSource(f'/vsicurl/use_head=no&url={dataset.content.url}')
        serializer = self.get_serializer(tile_source)
        return Response(serializer.data)


class TileSchemaGenerator(SwaggerAutoSchema):
    def get_produces(self):
        return ['image/png']


class TileView(GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Dataset.objects.filter(content__isnull=False, dataset_type='tile_source')
    model = Dataset
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: 'Image file', 404: 'Image tile not found'},
        auto_schema=TileSchemaGenerator,
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description='A UUID string identifying this dataset.',
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
        tile_source = GDALFileTileSource(f'/vsicurl/use_head=no&url={dataset.content.url}', encoding='PNG')
        try:
            tile = tile_source.getTile(x, y, z)
        except TileSourceError as e:
            error_msg = str(e)
            for missing_msg in (
                'z layer does not exist',
                'x is outside layer',
                'y is outside layer',
            ):
                if missing_msg in error_msg:
                    return Response(status=404)
            raise APIException(error_msg)
        return HttpResponse(tile, content_type='image/png')


urlpatterns = [
    path('datasets/<str:pk>/tiles/metadata', TileMetadataView.as_view()),
    path('datasets/<str:pk>/tiles/<int:z>/<int:x>/<int:y>.png', TileView.as_view()),
]
