from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    Investigation,
    InvestigationDetailSerializer,
    InvestigationSerializer,
    JobDetailSerializer,
    PinSerializer,
)


class InvestigationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Investigation.objects.all().order_by('name')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InvestigationDetailSerializer
        else:
            return InvestigationSerializer

    @swagger_auto_schema(responses={200: PinSerializer(many=True)})
    @action(detail=True, methods=['GET'])
    def pins(self, request, pk=None):
        payload = PinSerializer(self.get_object().pins.all(), many=True).data
        return Response(payload, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: JobDetailSerializer(many=True)})
    @action(detail=True, methods=['GET'])
    def jobs(self, request, pk=None):
        payload = JobDetailSerializer(self.get_object().jobs.all(), many=True).data
        return Response(payload, status=status.HTTP_200_OK)
