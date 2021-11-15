from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    Investigation,
    InvestigationDetailSerializer,
    InvestigationSerializer,
)


class InvestigationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    model = Investigation
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InvestigationDetailSerializer
        else:
            return InvestigationSerializer

    def get_queryset(self):
        investigations = get_objects_for_user(
            self.request.user,
            [f'core.{perm}' for perm in Investigation.get_read_permission_groups()],
            any_perm=True,
        )
        return investigations.all()
