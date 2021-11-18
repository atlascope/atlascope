from guardian.shortcuts import get_objects_for_user
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import Investigation, Pin, PinSerializer


class PinViewSet(GenericViewSet):
    model = Pin
    serializer_class = PinSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        visible_investigations = get_objects_for_user(
            self.request.user,
            [f'core.{perm}' for perm in Investigation.get_read_permission_groups()],
            any_perm=True,
        )
        owned_investigations = Investigation.objects.filter(owner=self.request.user)
        investigations = visible_investigations | owned_investigations
        return Pin.objects.filter(connection_pins__investigation__in=investigations)
