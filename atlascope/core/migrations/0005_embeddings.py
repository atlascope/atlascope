# Generated by Django 3.2.11 on 2022-02-22 14:47

import uuid

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_datasets'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetEmbedding',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('child_bounding_box', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                (
                    'child',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='parent_embeddings',
                        to='core.dataset',
                    ),
                ),
                (
                    'context',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='core.investigation'
                    ),
                ),
                (
                    'parent',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='child_embeddings',
                        to='core.dataset',
                    ),
                ),
            ],
        ),
    ]