# Generated by Django 3.2.11 on 2022-02-12 00:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

import atlascope.core.models.job


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_base_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'job_type',
                    models.CharField(
                        default='average_color',
                        max_length=100,
                        validators=[atlascope.core.models.job.validate_job_type],
                    ),
                ),
                ('additional_inputs', models.JSONField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='jobrunoutputimage',
            name='job_run',
        ),
        migrations.DeleteModel(
            name='JobRun',
        ),
        migrations.DeleteModel(
            name='JobRunOutputImage',
        ),
        migrations.DeleteModel(
            name='JobScript',
        ),
        migrations.AddField(
            model_name='job',
            name='original_dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.dataset'),
        ),
    ]
