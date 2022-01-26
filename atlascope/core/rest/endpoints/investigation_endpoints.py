from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import get_objects_for_user
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    Investigation,
    InvestigationDetailSerializer,
    InvestigationSerializer,
    PinSerializer,
)
from atlascope.core.rest.permissions import object_permission_required


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
        visible_investigations = get_objects_for_user(
            self.request.user,
            [f'core.{perm}' for perm in Investigation.get_read_permission_groups()],
            any_perm=True,
        )
        owned_investigations = Investigation.objects.filter(owner=self.request.user)
        investigations = visible_investigations | owned_investigations
        return investigations.all().order_by('name')

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'owner': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='the username of the owner of this investigation',
                ),
                'observers': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description='a list of the usernames of users who should '
                    'have only read access on this investigation',
                ),
                'investigators': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description='a list of the usernames of users who should '
                    'have write access on this investigation',
                ),
            },
        ),
        responses={200: InvestigationDetailSerializer()},
    )
    @object_permission_required(edit_access=True)
    @action(detail=True, methods=['POST'])
    def permissions(self, request, pk=None):
        """Update the lists of users that have permissions on this Investigation."""
        investigation: Investigation = self.get_object()
        data = request.data
        try:
            if 'owner' in data:
                investigation.owner = User.objects.get(username=data['owner'])
                investigation.save()
            if 'observers' in data:
                investigation.update_group('view_investigation', data['observers'])
            if 'investigators' in data:
                investigation.update_group('change_investigation', data['investigators'])
        except User.DoesNotExist:
            return Response(
                'Failed to save. Username not found.', status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError:
            return Response('Failed to save.', status=status.HTTP_400_BAD_REQUEST)

        payload = InvestigationDetailSerializer(investigation).data
        payload = {k: v for k, v in payload.items() if k in ['owner', 'investigators', 'observers']}
        return Response(payload, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: PinSerializer(many=True)})
    @object_permission_required(edit_access=True)
    @action(detail=True, methods=['GET'])
    def pins(self, request, pk=None):
        payload = PinSerializer(self.get_object().pins.all(), many=True).data
        return Response(payload, status=status.HTTP_200_OK)
