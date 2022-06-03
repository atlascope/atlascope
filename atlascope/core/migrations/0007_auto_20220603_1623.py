# Generated by Django 3.2.13 on 2022-06-03 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0006_merge_20220527_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pin',
            old_name='child_location',
            new_name='location',
        ),
        migrations.RemoveField(
            model_name='pin',
            name='child',
        ),
        migrations.RemoveField(
            model_name='pin',
            name='note',
        ),
        migrations.AddField(
            model_name='pin',
            name='polymorphic_ctype',
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='polymorphic_core.pin_set+',
                to='contenttypes.contenttype',
            ),
        ),
        migrations.CreateModel(
            name='NotePin',
            fields=[
                (
                    'pin_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='core.pin',
                    ),
                ),
                ('note', models.TextField(max_length=1000)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('core.pin',),
        ),
        migrations.CreateModel(
            name='DatasetPin',
            fields=[
                (
                    'pin_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='core.pin',
                    ),
                ),
                ('description', models.TextField(blank=True, max_length=1000)),
                (
                    'child',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='locations',
                        to='core.dataset',
                    ),
                ),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('core.pin',),
        ),
    ]
