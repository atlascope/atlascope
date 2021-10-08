from uuid import uuid4

from django.contrib import admin
from django.db import models
from rest_framework import serializers


class ContextMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    datasets = models.ManyToManyField('Dataset', related_name='context_datasets')


class ContextMapSerializer(serializers.HyperlinkedModelSerializer):
    datasets = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='dataset-detail'
    )

    class Meta:
        model = ContextMap
        fields = '__all__'


@admin.register(ContextMap)
class ContextMapAdmin(admin.ModelAdmin):
    pass
