from uuid import uuid4

from django.contrib import admin
from django.db import models
from rest_framework import serializers
from s3_file_field import S3FileField


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    script_contents = S3FileField(null=True)
    input_image = S3FileField(null=True)
    other_inputs = models.JSONField(null=True)
    outputs = models.JSONField(null=True)
    last_run = models.DateTimeField(null=True)
    preview_visual = S3FileField(null=True)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
