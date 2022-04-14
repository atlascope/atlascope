from itertools import cycle

from django_large_image.rest.viewsets import LargeImageDetailMixin
from large_image.exceptions import TileSourceError
from large_image.tilesource import FileTileSource
from large_image_source_ometiff import OMETiffFileTileSource
from large_image_source_tiff import TiffFileTileSource
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import Dataset, DatasetSerializer


class DatasetTileSourceView(GenericViewSet, LargeImageDetailMixin):
    queryset = Dataset.objects.filter(content__isnull=False, dataset_type='tile_source')
    serializer_class = DatasetSerializer

    default_colors = ['#ffffff']

    def get_path(self, *args, **kwargs) -> str:
        """Retreive path to image file from data record."""
        dataset = self.get_object()
        try:
            return str(dataset.content.path)
        except (AttributeError, ValueError):
            # Raise 400-level error as this dataset has no content
            raise ValidationError('Dataset has not content.')

    def open_tile_source(self, path: str, *args, **kwargs) -> FileTileSource:
        """Override to manually choose tile source class."""
        try:
            tile_source = OMETiffFileTileSource(path, *args, **kwargs)
        except TileSourceError:
            tile_source = TiffFileTileSource(path, *args, **kwargs)
        return tile_source

    def get_style(self, request: Request) -> dict:
        """Override django-large-image style parsing for cutom frame stuff.

        This builds a style dictionary for large-image following:

            https://girder.github.io/large_image/tilesource_options.html#style

        """
        channels = request.query_params.get('channels')
        if channels:
            channels = channels.split(',')
        else:
            tile_source = self.open_tile_source(self.get_path())  # TODO: better handle upstream
            channels = range(len(tile_source.getMetadata()['frames']))
        colors = request.query_params.get('colors')
        if colors:
            colors = [f'#{color}' for color in colors.split(',')]
        else:
            colors = self.default_colors
        style = {'bands': []}
        for channel, color in list(zip(channels, cycle(colors))):
            style['bands'].append(
                {
                    'frame': channel,
                    'palette': ['#000', color],
                }
            )
        return style


router = DefaultRouter(trailing_slash=False)
router.register(r'datasets/tile_source', DatasetTileSourceView, basename='tile_source')

urlpatterns = router.urls
