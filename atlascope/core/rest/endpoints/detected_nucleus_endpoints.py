from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import DetectedNucleus, DetectedNucleusSerializer
from atlascope.core.models.detected_nucleus import SimilarNucleusSerializer, similar_nuclei


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

    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        nucleus = self.get_object()
        queryset = similar_nuclei(nucleus)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SimilarNucleusSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SimilarNucleusSerializer(queryset, many=True)
        return Response(serializer.data)
