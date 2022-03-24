from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    DatasetEmbeddingSerializer,
    Investigation,
    InvestigationSerializer,
    JobDetailSerializer,
    PinSerializer,
    TourSerializer,
    TourCreateSerializer,
    Tour,
)


class InvestigationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Investigation.objects.all().order_by('id')
    serializer_class = InvestigationSerializer

    @swagger_auto_schema(responses={200: PinSerializer(many=True)})
    @action(detail=True, methods=['GET'])
    def pins(self, request, pk=None):
        payload = PinSerializer(self.get_object().pins.all().order_by('id'), many=True).data
        return Response(payload, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: JobDetailSerializer(many=True)})
    @action(detail=True, methods=['GET'])
    def jobs(self, request, pk=None):
        payload = JobDetailSerializer(self.get_object().jobs.all().order_by('id'), many=True).data
        return Response(payload, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: DatasetEmbeddingSerializer(many=True)})
    @action(detail=True, methods=['GET'])
    def embeddings(self, request, pk=None):
        payload = DatasetEmbeddingSerializer(self.get_object().embeddings.all(), many=True).data
        return Response(payload, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TourCreateSerializer())
    @action(detail=True, methods=['POST'])
    def tour(self, request, pk=None):
        serializer = TourCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data['way_points'])

        tour = Tour(investigation=self.get_object(), way_points=serializer.validated_data['way_points'])
        tour.save()

        return Response(TourSerializer(tour).data, status=status.HTTP_201_CREATED)
