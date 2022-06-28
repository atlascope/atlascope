import os
from pathlib import Path
import tempfile

from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from large_image_source_ometiff import OMETiffFileTileSource, TiffFileTileSource, TileSourceError
from rest_framework import serializers
from tifftools.commands import tiff_concat

from atlascope.core.importers import available_importers


class Dataset(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, blank=True)
    content = models.FileField(null=True)
    metadata = models.JSONField(null=True)
    dataset_type = models.CharField(
        max_length=20,
        choices=[(choice, choice) for choice in settings.DATASET_TYPES],
        default=settings.DATASET_TYPES[0],
    )
    source_dataset = models.ForeignKey(
        'Dataset',
        null=True,
        on_delete=models.PROTECT,
        related_name='derived_datasets',
    )

    def perform_import(self, importer="UploadImporter", **kwargs):
        importer_obj = available_importers[importer]()
        importer_obj.run(**kwargs)

        self.content.save(
            f'{self.name.replace(" ","_")}_{str(self.id)}',
            importer_obj.content,
        )
        self.metadata = importer_obj.metadata
        if not self.name:
            self.name = importer_obj.dataset_name or f'{importer} {self.id}'

    def subimage(self, investigation, x0: int, x1: int, y0: int, y1: int) -> 'Dataset':
        cropped_metadata = {
            'subimage_bbox': {
                'x0': x0,
                'x1': x1,
                'y0': y0,
                'y1': y1,
            }
        }

        try:
            src = OMETiffFileTileSource(self.content.path)
        except TileSourceError:
            src = TiffFileTileSource(self.content.path)
        src_metadata = src.getMetadata()
        cropped_frames_locations = []
        for frame in src_metadata['frames']:
            result, mime = src.getRegion(
                region=dict(left=x0, right=x1, top=y0, bottom=y1),
                encoding='TILED',
                frame=frame['Frame'],
                shrinkMode='mode',
            )
            cropped_frames_locations.append(result)

        with tempfile.TemporaryDirectory() as tmpdirname:
            dest = Path(tmpdirname, 'composite.tiff')
            tiff_concat(cropped_frames_locations, dest)

            dataset = Dataset(
                name=f'{self.name} Subimage ({x0}, {y0}) -> ({x1}, {y1})',
                metadata=cropped_metadata,
                source_dataset=self,
                dataset_type="subimage",
            )
            dataset.save()
            content_filename = f'cropped_{dataset.id}_{self.content.name}'
            dataset.content.save(content_filename, open(dest, 'rb'))
            investigation.datasets.add(dataset)
            investigation.save()

            return dataset


@receiver(models.signals.post_delete, sender=Dataset)
def delete_file(sender, instance, *args, **kwargs):
    if instance.content and os.path.isfile(instance.content.path):
        os.remove(instance.content.path)


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'id',
            'name',
            'description',
            'content',
            'metadata',
            'dataset_type',
            'source_dataset',
            'derived_datasets',
            'child_embeddings',
            'parent_embeddings',
            'jobs',
            'origin',
            'pins',
            'locations',
            'detected_nuclei',
        ]

    def to_representation(self, instance):
        """Only include detected_nuclei field on nucleus_detection type Datasets."""
        ret = super().to_representation(instance)
        if ret['dataset_type'] != 'nucleus_detection':
            del ret['detected_nuclei']
        return ret


class DatasetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'name',
            'description',
            'dataset_type',
            'importer',
            'import_arguments',
        ]

    def validate(self, data):
        if data['importer'] not in available_importers:
            raise ValidationError(
                f'Importer value must be '
                f'one of the following installed importers'
                f': {str(list(available_importers.keys()))}'
            )
        importer_obj = available_importers[data['importer']]()
        importer_obj.validate_arguments(**data['import_arguments'])
        return data

    def create(self, validated_data):
        true_data = {
            k: v for k, v in validated_data.items() if k not in ['importer', 'import_arguments']
        }
        return super().create(true_data)

    name = serializers.CharField(required=False)
    importer = serializers.CharField(
        default='UploadImporter',
        help_text=f"The importer module to invoke.\
            Must be one of {str(list(available_importers.keys()))}.",
    )
    import_arguments = serializers.JSONField(
        required=True,
        help_text="Any arguments to supply to the selected importer function",
    )


class InvestigationRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        from atlascope.core.models import Investigation

        return Investigation.objects.all()


class DatasetSubImageSerializer(serializers.Serializer):
    x0 = serializers.IntegerField(required=True)
    y0 = serializers.IntegerField(required=True)
    x1 = serializers.IntegerField(required=True)
    y1 = serializers.IntegerField(required=True)
    investigation = InvestigationRelatedField(required=True)


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
