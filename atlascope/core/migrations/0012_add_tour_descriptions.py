# Generated by Django 3.2.15 on 2022-08-29 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_detected_structures'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='waypoint',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]