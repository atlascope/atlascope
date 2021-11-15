from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from atlascope.core.models import (
    ConnectionsMap,
    ConnectionsMapSerializer,
    ContextMap,
    ContextMapSerializer,
    Dataset,
    DatasetSerializer,
    Investigation,
    InvestigationSerializer,
    Pin,
    PinSerializer,
)
from atlascope.core.rest.additional_serializers import UserSerializer


class APIRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response(
            {
                endpoint.name: reverse(endpoint.name, request=request)
                for endpoint in [
                    InvestigationList,
                    DatasetList,
                    PinList,
                    UserList,
                ]
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


class ContextMapDetail(generics.RetrieveUpdateAPIView):
    queryset = ContextMap.objects.all()
    serializer_class = ContextMapSerializer
    name = 'context-map-detail'


class ConnectionsMapDetail(generics.RetrieveUpdateAPIView):
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


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
