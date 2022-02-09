from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    JobScript,
    JobScriptSerializer,
)


class JobScriptViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    model = JobScript
    queryset = JobScript.objects.all().order_by('name')
    serializer_class = JobScriptSerializer
    permission_classes = [IsAuthenticated]
