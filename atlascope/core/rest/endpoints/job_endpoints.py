from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from atlascope.core.job_types import available_job_types
from atlascope.core.models import Job, JobDetailSerializer, JobSpawnSerializer


class JobViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    model = Job
    queryset = Job.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.action in ['create', 'rerun']:
            return JobSpawnSerializer
        return JobDetailSerializer

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job: Job = serializer.save()
        job.spawn()

        return Response(JobDetailSerializer(job).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=no_body,
        responses={204: 'Rerun spawned.'},
    )
    @action(detail=True, methods=['POST'])
    def rerun(self, request, **kwargs):
        job: Job = self.get_object()
        job.spawn()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description='Retrieve a list of available options for job_type on Jobs',
        manual_parameters=[],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)},
    )
    @action(detail=False, methods=['GET'])
    def types(self, request, **kwargs):
        payload = [
            {
                'name': key,
                'description': module.__doc__,
                'schema': module.schema,
            }
            for key, module in available_job_types.items()
        ]
        return Response(payload)
