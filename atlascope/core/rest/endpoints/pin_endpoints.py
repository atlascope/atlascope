from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import Pin, PinSerializer


class PinViewSet(GenericViewSet):
    model = Pin
    serializer_class = PinSerializer
    queryset = Pin.objects.all().order_by('id')
