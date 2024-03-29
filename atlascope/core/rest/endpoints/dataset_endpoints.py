import os

from django.http import FileResponse, Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    Dataset,
    DatasetCreateSerializer,
    DatasetSerializer,
    DatasetSubImageSerializer,
)


class ContentRenderer(BaseRenderer):
    media_type = 'image/png'
    format = 'png'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class PassthroughRenderer(BaseRenderer):
    media_type = 'application/octet-stream'
    format = ''

    def render(self, data, media_type=None, renderer_context=None):
        return data


class DatasetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Dataset.objects.all().order_by('id')
    serializer_class = DatasetSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return DatasetCreateSerializer
        else:
            return DatasetSerializer

    @swagger_auto_schema(request_body=DatasetCreateSerializer())
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_dataset_obj = serializer.save()
        new_dataset_obj.perform_import(
            request.data['importer'],
            **request.data['import_arguments'],
        )

        return Response(DatasetSerializer(new_dataset_obj).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=DatasetSubImageSerializer())
    @action(detail=True, methods=['POST'])
    def subimage(self, request, pk):
        serializer = DatasetSubImageSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        original = self.get_object()
        subimage = original.subimage(**serializer.validated_data)

        return Response(DatasetSerializer(subimage).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'], renderer_classes=(PassthroughRenderer,))
    def download(self, request, pk):
        dataset = self.get_object()
        try:
            path = dataset.content.path
        except (AttributeError, ValueError):
            raise ValidationError('Dataset has no content')
        if os.path.exists(path):
            response = FileResponse(open(path, 'rb'), content_type='application/octet-stream')
            response['Content-Length'] = dataset.content.size
            response['Content-Disposition'] = f'attachment; filename={dataset.content.name}'
            return response
        raise Http404
