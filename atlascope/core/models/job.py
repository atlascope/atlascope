from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework import serializers

from atlascope.core.job_types import available_job_types


def validate_job_type(value):
    if value not in available_job_types:
        raise ValidationError(
            f'Job Type value must be '
            f'one of the following installed job types'
            f': {str(list(available_job_types.keys()))}'
        )


class Job(models.Model):
    complete = models.BooleanField(default=False)
    failure = models.CharField(blank=True, max_length=255)
    investigation = models.ForeignKey(
        'Investigation',
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    job_type = models.CharField(
        default='average_color',
        max_length=100,
        validators=[validate_job_type],
    )
    original_dataset = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    resulting_datasets = models.ManyToManyField(
        'Dataset',
        related_name='origin',
    )
    additional_inputs = models.JSONField(null=True)

    def spawn(self):
        runner = available_job_types[self.job_type].run
        runner.delay(
            # celery arguments must be serializable
            self.id,
            self.original_dataset.id,
            **self.additional_inputs or {},
        )


class JobSpawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'investigation',
            'job_type',
            'original_dataset',
            'additional_inputs',
        ]


class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_type', 'complete')
