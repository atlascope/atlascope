from django_large_image.rest.viewsets import LargeImageDetailMixin
from large_image.exceptions import TileSourceError
from large_image.tilesource import FileTileSource
from large_image_source_ometiff import OMETiffFileTileSource
from large_image_source_pil import PILFileTileSource
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

    def open_tile_source(self, request: Request, path: str, **kwargs) -> FileTileSource:
        """Override to manually choose tile source class."""
        try:
            tile_source = OMETiffFileTileSource(path, **kwargs)
        except TileSourceError:
            tile_source = TiffFileTileSource(path, **kwargs)
        return tile_source


router = DefaultRouter(trailing_slash=False)
router.register(r'datasets/tile_source', DatasetTileSourceView, basename='tile_source')

urlpatterns = router.urls
