from uuid import uuid4

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import serializers
from s3_file_field import S3FileField

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
    job_type = models.CharField(
        default='average_color', max_length=100, validators=[validate_job_type]
    )
    original_dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE)
    additional_inputs = models.JSONField(null=True)
    outputs = models.JSONField(null=True)
    last_run = models.DateTimeField(null=True)

    def spawn(self):
        runner = available_job_types[self.job_type]
        runner.delay(
            # celery arguments must be serializable
            original_dataset_id=self.original_dataset.id,
            **self.additional_inputs or {},
        )


class JobRunSpawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRun
        fields = ['original_dataset', 'additional_inputs', 'job_type']


class JobRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRun
        fields = '__all__'


@admin.register(JobRun)
class JobRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_type', 'last_run')
