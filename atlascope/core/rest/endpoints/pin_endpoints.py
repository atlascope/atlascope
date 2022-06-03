from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import Pin, BasePinSerializer


class PinViewSet(GenericViewSet):
    model = Pin
    serializer_class = BasePinSerializer
    queryset = Pin.objects.all().order_by('id')
