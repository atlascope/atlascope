from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    Dataset,
    DatasetCreateSerializer,
    DatasetSerializer,
    DatasetSubImageSerializer,
)


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

    @swagger_auto_schema(request_body=DatasetSubImageSerializer())
    @action(detail=False, methods=['POST'])
    def create_sub_image(self, request):
        serializer = DatasetSubImageSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        original_dataset = Dataset.objects.get(id=serializer.validated_data["original_dataset_id"])
        meta = serializer.validated_data.copy()
        meta.pop("original_dataset_id")
        new_dataset_obj = Dataset(
            name=f'{original_dataset.name} Sub Image',
            metadata=meta,
            source_dataset=original_dataset,
            dataset_type="sub_image",
        )
        new_dataset_obj.save()

        return Response(DatasetSerializer(new_dataset_obj).data, status=status.HTTP_201_CREATED)
