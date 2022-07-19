from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import DetectedStructure, DetectedStructureSerializer


class DetectedStructureViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = DetectedStructureSerializer

    def get_queryset(self):
        detection_dataset_id = self.request.query_params.get('detection_dataset')
        if detection_dataset_id:
            return DetectedStructure.objects.filter(
                detection_dataset__id=detection_dataset_id,
            )
        return DetectedStructure.objects.all()
