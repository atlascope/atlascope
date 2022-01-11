from uuid import uuid4

from django.contrib import admin
from django.db import models
from rest_framework import serializers
from s3_file_field import S3FileField


class JobRunOutputImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    job_run = models.ForeignKey('JobRun', on_delete=models.CASCADE, related_name="output_images")
    stored_image = S3FileField(null=True)


class JobRunOutputImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRunOutputImage
        fields = '__all__'


@admin.register(JobRunOutputImage)
class JobRunOutputImageAdmin(admin.ModelAdmin):
    list_display = ('id',)
