from typing import List
from uuid import uuid4

from django.contrib import admin
from django.db import models
from django_extensions.db.models import TimeStampedModel
from rest_framework import serializers


class Investigation(TimeStampedModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, blank=True)
    datasets = models.ManyToManyField('Dataset', related_name='investigations')
    notes = models.TextField(max_length=5000, blank=True)


class InvestigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigation
        fields = ('id', 'name', 'description')


class InvestigationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investigation
        fields = [
            'id',
            'name',
            'description',
            'datasets',
            'pins',
            'notes',
            'created',
            'modified',
            'embeddings',
            'jobs',
        ]


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('created', 'modified')
