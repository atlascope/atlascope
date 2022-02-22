from uuid import uuid4

from django.contrib import admin
from django.contrib.gis.db.models import PolygonField
from django.db import models
from rest_framework import serializers


class DatasetEmbedding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    context = models.ForeignKey('Investigation', on_delete=models.CASCADE)
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
        return f'Embedding {self.child.name} in {self.parent.name} ({self.context.name})'


class DatasetEmbeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetEmbedding
        fields = '__all__'


@admin.register(DatasetEmbedding)
class DatasetEmbeddingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'context',
        'parent',
        'child',
    )
