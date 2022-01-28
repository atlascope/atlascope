from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    Dataset,
    DatasetSerializer,
    DatasetCreateImportSerializer,
    DatasetCreateUploadSerializer,
)


class DatasetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    model = Dataset
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        visible_datasets = get_objects_for_user(
            self.request.user,
            [f'core.{perm}' for perm in Dataset.get_read_permission_groups()],
            any_perm=True,
        )
        public_datasets = Dataset.objects.filter(public=True)
        datasets = visible_datasets | public_datasets
        return datasets.all().order_by('name')

    # TODO: We can't acheive multiple request_body schema options for one endpoint.
    # Should we split to two endpoints?
    # Or keep a combined schema wherein some fields will always be non-applicable?
    @swagger_auto_schema(
        request_body=DatasetCreateImportSerializer or DatasetCreateUploadSerializer
    )
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_dataset_obj = serializer.save()

        if not new_dataset_obj.content:
            if not new_dataset_obj.importer:
                raise APIException("Missing required fields: Specify either content or importer.")
            if 'importer_arguments' not in request.data:
                raise APIException(
                    "Missing required fields: Specify importer_arguments as a nested object."
                )
            new_dataset_obj.perform_import(**request.data['importer_arguments'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)
