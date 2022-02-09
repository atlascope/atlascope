from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from atlascope.core.tasks import spawn_job

from atlascope.core.models import (
    Dataset,
    DatasetCreateSerializer,
    DatasetSerializer,
    JobSpawnSerializer
    )


class DatasetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    model = Dataset
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return DatasetCreateSerializer
        else:
            return DatasetSerializer

    def get_queryset(self):
        visible_datasets = get_objects_for_user(
            self.request.user,
            [f'core.{perm}' for perm in Dataset.get_read_permission_groups()],
            any_perm=True,
        )
        public_datasets = Dataset.objects.filter(public=True)
        datasets = visible_datasets | public_datasets
        return datasets.all().order_by('name')

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

    @swagger_auto_schema(request_body=JobSpawnSerializer(), responses={204: 'Job Spawned'})
    @action(detail=False, methods=['POST'])
    def run_job(self, request, **kwargs):
        serializer = JobSpawnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        spawn_job(serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT)
