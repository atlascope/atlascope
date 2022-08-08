# Generated by Django 3.2.13 on 2022-07-29 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_pin_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='dataset_type',
            field=models.CharField(
                choices=[
                    ('tile_source', 'tile_source'),
                    ('tile_overlay', 'tile_overlay'),
                    ('analytics', 'analytics'),
                    ('subimage', 'subimage'),
                    ('nucleus_detection', 'nucleus_detection'),
                    ('non_tiled_image', 'non_tiled_image'),
                    ('3d_volume', '3d_volume'),
                ],
                default='tile_source',
                max_length=20,
            ),
        ),
    ]