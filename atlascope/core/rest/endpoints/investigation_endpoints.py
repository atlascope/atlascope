from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import get_objects_for_user
from django.contrib.auth.models import User
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from atlascope.core.models import (
    Investigation,
    InvestigationDetailSerializer,
    InvestigationSerializer,
)
from atlascope.core.rest.permissions import investigation_permission_required


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
    @investigation_permission_required(edit_access=True)
    @action(detail=True, methods=['POST'])
    def permissions(self, request, pk=None):
        """Update the lists of users that have permissions on this Investigation."""
        investigation: Investigation = self.get_object()
        data = request.data
        print(data)
        try:
            if 'owner' in data:
                investigation.owner = User.objects.get(username=data['owner'])
                investigation.save()
            if 'observers' in data:
                investigation.update_group('view_investigation', data['observers'])
            if 'investigators' in data:
                investigation.update_group('change_investigation', data['observers'])
        except User.DoesNotExist:
            return Response(
                'Failed to save. Username not found.', status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError:
            return Response('Failed to save.', status=status.HTTP_400_BAD_REQUEST)

        payload = InvestigationDetailSerializer(investigation).data
        return Response(payload, status=status.HTTP_200_OK)
