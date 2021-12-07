from drf_yasg.utils import no_body, swagger_auto_schema
from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import Dataset, DatasetSerializer
from atlascope.core.rest.permissions import object_permission_required


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

    @swagger_auto_schema(
        request_body=no_body,
        responses={204: 'Import successful.'},
    )
    @object_permission_required(model=Dataset)
    @action(
        detail=True,
        methods=['POST'],
        url_path='import',
    )
    def perform_import(self, request, **kwargs):
        dataset: Dataset = self.get_object()
        dataset.perform_import()
        return Response(status=status.HTTP_204_NO_CONTENT)
