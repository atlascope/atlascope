# Generated by Django 3.2.12 on 2022-03-30 17:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_dataset_dataset_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('zoom', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('way_points', models.ManyToManyField(through='core.Investigation', to='core.Waypoint')),
            ],
        ),
        migrations.AddField(
            model_name='investigation',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tour'),
        ),
        migrations.AddField(
            model_name='investigation',
            name='way_point',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.waypoint'),
        ),
    ]
