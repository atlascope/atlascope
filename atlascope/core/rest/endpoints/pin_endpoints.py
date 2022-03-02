from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import Investigation, Pin, PinSerializer


class PinViewSet(GenericViewSet):
    model = Pin
    serializer_class = PinSerializer

    def get_queryset(self):
        investigations = Investigation.objects.all()
        return Pin.objects.filter(connection_pins__investigation__in=investigations)
