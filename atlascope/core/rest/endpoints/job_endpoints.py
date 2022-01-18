from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.models import (
    JobRun,
    JobRunSerializer,
    JobRunSpawnSerializer,
    JobScript,
    JobScriptSerializer,
)


class JobScriptViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    model = JobScript
    queryset = JobScript.objects.all()
    serializer_class = JobScriptSerializer
    permission_classes = [IsAuthenticated]


class JobRunViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    model = JobRun
    queryset = JobRun.objects.all()
    serializer_class = JobRunSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=JobRunSpawnSerializer,
        manual_parameters=[
            openapi.Parameter(
                'other_inputs',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_OBJECT,
            )
        ],
        responses={204: 'Import successful.'},
    )
    @action(
        detail=False,
        methods=['POST'],
        parser_classes=(MultiPartParser,),
    )
    def spawn(self, request, **kwargs):
        # TODO: image is unsigned when sent through Swagger
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job_run: JobRun = serializer.save()
        job_run.spawn()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=no_body,
        responses={204: 'Import successful.'},
    )
    @action(detail=True, methods=['POST'])
    def rerun(self, request, **kwargs):
        job_run: JobRun = self.get_object()
        job_run.spawn()

        return Response(status=status.HTTP_204_NO_CONTENT)
