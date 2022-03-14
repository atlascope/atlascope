from uuid import uuid4

from django.contrib import admin
from django.contrib.gis.db.models import PolygonField
from django.db import models
from rest_framework import serializers


class DatasetEmbedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    investigation = models.ForeignKey(
        'Investigation',
        on_delete=models.CASCADE,
        related_name='embeddings',
    )
    parent = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
        related_name='child_embeddings',
    )
    child = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
        related_name='parent_embeddings',
    )
    child_bounding_box = PolygonField()

    def __str__(self):
        return f'Embedding {self.child.name} in {self.parent.name} ({self.investigation.name})'


class DatasetEmbeddingSerializer(serializers.ModelSerializer):
    child_bounding_box = serializers.ListField(
        source='child_bounding_box.extent',
        child=serializers.FloatField(),
        min_length=4,
        max_length=4,
        read_only=True,
    )

    class Meta:
        model = DatasetEmbedding
        fields = '__all__'


@admin.register(DatasetEmbedding)
class DatasetEmbeddingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'investigation',
        'parent',
        'child',
    )
