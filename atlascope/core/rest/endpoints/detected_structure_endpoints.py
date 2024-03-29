from PIL import Image
from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q
from django.http import HttpResponse
from matplotlib import cm
import numpy as np
from rest_framework import mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import DetectedStructure, DetectedStructureSerializer
from atlascope.core.models.detected_structure import SimilarNucleusSerializer, similar_nuclei


class DetectedStructureViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = DetectedStructureSerializer
    pagination_class = None

    def get_queryset(self):
        detection_dataset_id = self.request.query_params.get('detection_dataset')
        if detection_dataset_id:
            return DetectedStructure.objects.filter(
                detection_dataset__id=detection_dataset_id,
            )
        return DetectedStructure.objects.all()

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

    @action(detail=True, methods=['get'])
    def fingerprint(self, request, pk=None):
        nucleus = self.get_object()
        # fingerprint array of floats (100x1)
        array = np.array(nucleus.fingerprint)
        # normalize array to 0-1 floats
        normalized_array = (array - np.min(array)) / (np.max(array) - np.min(array))
        # reshape to 10x10 matrix (same row ordering as source image)
        image_matrix = np.reshape(normalized_array, (10, 10))
        # apply colormap to matrix to better see the contrasts
        color_mapped_matrix = cm.turbo(image_matrix)
        # convert matrix floats to ints for PIL
        int_color_mapped_matrix = (color_mapped_matrix * 255).astype('uint8')
        # create image from matrix
        image = Image.fromarray(int_color_mapped_matrix)
        # create buffer response for image
        response = HttpResponse(content_type='image/png')
        # save image to buffer
        image.save(response, format='PNG')
        return response


@api_view()
def get_similar_nuclei(request, dataset: int, x: str, y: str):
    # return 5 most similar nuclei to the nucleus located at x,y
    queryset = DetectedStructure.objects.filter(structure_type="nucleus").filter(
        Q(detection_dataset=dataset) | Q(detection_dataset__source_dataset=dataset)
    )
    nucleus = queryset.order_by(
        GeometryDistance('centroid', GEOSGeometry(f'POINT({float(x)} {float(y)})', srid=4326))
    ).first()
    queryset = similar_nuclei(nucleus, queryset)[:6]
    serializer = SimilarNucleusSerializer(queryset, many=True)
    return Response(serializer.data)
