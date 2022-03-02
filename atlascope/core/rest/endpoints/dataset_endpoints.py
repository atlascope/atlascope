from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import Dataset, DatasetCreateSerializer, DatasetSerializer


class DatasetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Dataset.objects.all().order_by('name')
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
