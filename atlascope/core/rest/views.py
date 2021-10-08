from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from atlascope.core.models import (
    Investigation,
    InvestigationSerializer,
    ContextMap,
    ContextMapSerializer,
    ConnectionsMap,
    ConnectionsMapSerializer,
    Dataset,
    DatasetSerializer,
    Pin,
    PinSerializer,
)


# browsable API
class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'investigations': reverse(InvestigationList.name, request=request),
                'context-maps': reverse(ContextMapList.name, request=request),
                'connections-maps': reverse(ConnectionsMapList.name, request=request),
                'datasets': reverse(DatasetList.name, request=request),
                'pins': reverse(PinList.name, request=request),
            }
        )


class InvestigationList(generics.ListCreateAPIView):
    queryset = Investigation.objects.all()
    serializer_class = InvestigationSerializer
    name = 'investigation-list'


class InvestigationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Investigation.objects.all()
    serializer_class = InvestigationSerializer
    name = 'investigation-detail'


class ContextMapList(generics.ListCreateAPIView):
    queryset = ContextMap.objects.all()
    serializer_class = ContextMapSerializer
    name = 'context-map-list'


class ContextMapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContextMap.objects.all()
    serializer_class = ContextMapSerializer
    name = 'context-map-detail'


class ConnectionsMapList(generics.ListCreateAPIView):
    queryset = ConnectionsMap.objects.all()
    serializer_class = ConnectionsMapSerializer
    name = 'connections-map-list'


class ConnectionsMapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConnectionsMap.objects.all()
    serializer_class = ConnectionsMapSerializer
    name = 'connections-map-detail'


class DatasetList(generics.ListCreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    name = 'dataset-list'


class DatasetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    name = 'dataset-detail'


class PinList(generics.ListCreateAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    name = 'pin-list'


class PinDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    name = 'pin-detail'
