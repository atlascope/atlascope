from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from atlascope.core.models.importer import importers


class AtlascopeConfigView(APIView):
    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def get(self, request):
        payload = {
            'dataset_importer_options': list(importers.keys()),
        }
        return Response(payload, status=status.HTTP_200_OK)
