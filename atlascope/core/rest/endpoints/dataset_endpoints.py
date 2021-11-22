from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import Dataset, DatasetSerializer


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
