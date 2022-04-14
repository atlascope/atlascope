# Generated by Django 3.2.12 on 2022-04-04 21:55

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields

import atlascope.core.models.job


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_girder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name='created'
                    ),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name='modified'
                    ),
                ),
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=5000)),
                ('content', models.FileField(null=True, upload_to='')),
                ('metadata', models.JSONField(null=True)),
                (
                    'dataset_type',
                    models.CharField(
                        choices=[
                            ('tile_source', 'tile_source'),
                            ('tile_overlay', 'tile_overlay'),
                            ('analytics', 'analytics'),
                            ('subimage', 'subimage'),
                        ],
                        default='tile_source',
                        max_length=20,
                    ),
                ),
                (
                    'source_dataset',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='derived_datasets',
                        to='core.dataset',
                    ),
                ),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Investigation',
            fields=[
                (
                    'created',
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name='created'
                    ),
                ),
                (
                    'modified',
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name='modified'
                    ),
                ),
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=5000)),
                ('notes', models.TextField(blank=True, max_length=5000)),
                (
                    'datasets',
                    models.ManyToManyField(related_name='investigations', to='core.Dataset'),
                ),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('child_location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                (
                    'color',
                    models.CharField(
                        choices=[
                            ('red', 'red'),
                            ('blue', 'blue'),
                            ('green', 'green'),
                            ('orange', 'orange'),
                            ('purple', 'purple'),
                            ('black', 'black'),
                        ],
                        default='red',
                        max_length=15,
                    ),
                ),
                ('note', models.TextField(blank=True, max_length=1000)),
                (
                    'child',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='locations',
                        to='core.dataset',
                    ),
                ),
                (
                    'investigation',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='pins',
                        to='core.investigation',
                    ),
                ),
                (
                    'parent',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='pins',
                        to='core.dataset',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('complete', models.BooleanField(default=False)),
                (
                    'job_type',
                    models.CharField(
                        default='average_color',
                        max_length=100,
                        validators=[atlascope.core.models.job.validate_job_type],
                    ),
                ),
                ('additional_inputs', models.JSONField(null=True)),
                (
                    'investigation',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='jobs',
                        to='core.investigation',
                    ),
                ),
                (
                    'original_dataset',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='jobs',
                        to='core.dataset',
                    ),
                ),
                (
                    'resulting_datasets',
                    models.ManyToManyField(related_name='origin', to='core.Dataset'),
                ),
            ],
        ),
        migrations.CreateModel(
            name='DatasetEmbedding',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
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
                    'investigation',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='embeddings',
                        to='core.investigation',
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
