from uuid import uuid4

from django.contrib import admin
from django.db import models
from rest_framework import serializers
from s3_file_field import S3FileField


class JobScript(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    script_contents = S3FileField(null=True)


class JobScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobScript
        fields = ['id', 'name']


@admin.register(JobScript)
class JobScriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
