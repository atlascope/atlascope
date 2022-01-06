from uuid import uuid4

from django.contrib import admin
from django.db import models
from rest_framework import serializers
from s3_file_field import S3FileField


class JobRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    script = models.ForeignKey('JobScript', on_delete=models.CASCADE)
    input_image = S3FileField(null=True)
    other_inputs = models.JSONField(null=True)
    outputs = models.JSONField(null=True)
    last_run = models.DateTimeField(null=True)
    preview_visual = S3FileField(null=True)


class JobRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRun
        fields = '__all__'

    output_images = serializers.SerializerMethodField('get_output_images')

    def get_output_images(self, obj):
        return [output_image.stored_image for output_image in obj.output_images]


@admin.register(JobRun)
class JobRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'script', 'last_run')
