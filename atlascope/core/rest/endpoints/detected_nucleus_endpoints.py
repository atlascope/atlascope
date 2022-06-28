from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import DetectedNucleus, DetectedNucleusSerializer


class DetectedNucleusViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = DetectedNucleusSerializer

    def get_queryset(self):
        detection_dataset_id = self.request.query_params.get('detection_dataset')
        if detection_dataset_id:
            return DetectedNucleus.objects.filter(
                detection_dataset__id=detection_dataset_id,
            )
        return DetectedNucleus.objects.all()
