from uuid import uuid4

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import serializers
from s3_file_field import S3FileField

from atlascope.core.tasks import spawn_job
from atlascope.core.job_types import available_job_types


def validate_job_type(value):
    if value not in available_job_types:
        raise ValidationError(
            f'Job Type value must be '
            f'one of the following installed job types'
            f': {str(list(available_job_types.keys()))}'
        )


class JobRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    job_type = models.CharField(default='CloneData', max_length=100, validators=[validate_job_type])
    input_image = S3FileField(null=True)
    other_inputs = models.JSONField(null=True)
    outputs = models.JSONField(null=True)
    last_run = models.DateTimeField(null=True)
    preview_visual = S3FileField(null=True)

    def spawn(self):
        spawn_job.delay(str(self.id))


class JobRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRun
        fields = '__all__'


class JobRunSpawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRun
        fields = ['input_image', 'other_inputs', 'job_type']

    input_image = serializers.CharField()


@admin.register(JobRun)
class JobRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_type', 'last_run')
