from uuid import uuid4

from django.contrib import admin
from django.db import models
from guardian.admin import GuardedModelAdmin
from rest_framework import serializers


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, blank=True)
    public = models.BooleanField(default=True)
    source_uri = models.CharField(max_length=3000, null=False, blank=False)
    # import_function
    # scale
    # applicable_heuristics

    def get_read_permission_groups():
        return ['view_dataset', 'change_dataset']

    def get_write_permission_groups():
        return ['change_dataset']


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'


@admin.register(Dataset)
class DatasetAdmin(GuardedModelAdmin):
    list_display = ('id', 'source_uri')
