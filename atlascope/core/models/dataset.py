from uuid import uuid4

from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from guardian.admin import GuardedModelAdmin
from rest_framework import serializers
from s3_file_field import S3FileField

from .importer import importers


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, blank=True)
    public = models.BooleanField(default=True)
    content = S3FileField(null=True)
    metadata = models.JSONField(null=True)
    dataset_type = models.CharField(
        max_length=20,
        choices=[(choice, choice) for choice in settings.DATASET_TYPES],
        default=settings.DATASET_TYPES[0],
    )
    derived_datasets = models.ManyToManyField('Dataset', blank=True)
    # scale
    # applicable_heuristics

    def get_read_permission_groups():
        return ['view_dataset', 'change_dataset']

    def get_write_permission_groups():
        return ['change_dataset']

    def perform_import(self, importer="UploadImporter", **kwargs):
        importer_obj = importers[importer]()
        importer_obj.run(**kwargs)

        self.content.save(
            f'{self.name.replace(" ","_")}_{str(self.id)}',
            importer_obj.content,
        )
        self.metadata = importer_obj.metadata
        if not self.name:
            self.name = importer_obj.dataset_name or f'{importer} {self.id}'


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = '__all__'


class DatasetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'name',
            'description',
            'public',
            'dataset_type',
            'importer',
            'import_arguments',
        ]

    def validate(self, data):
        if data['importer'] not in importers:
            raise ValidationError(
                f'Importer value must be '
                f'one of the following installed importers'
                f': {str(list(importers.keys()))}'
            )
        importer_obj = importers[data['importer']]()
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
        help_text=f"The importer module to invoke. Must be one of {str(list(importers.keys()))}.",
    )
    import_arguments = serializers.JSONField(
        required=True,
        help_text="Any arguments to supply to the selected importer function",
    )


@admin.register(Dataset)
class DatasetAdmin(GuardedModelAdmin):
    list_display = ('id', 'name')
