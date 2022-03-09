import json
import os
from pathlib import Path

from django.contrib.gis.db.models import PointField, PolygonField
from django.contrib.gis.geos import Point
from django.contrib.gis.geos.polygon import Polygon
import djclick as click
from rest_framework.serializers import ValidationError

from atlascope.core.models import Dataset, DatasetEmbedding, Investigation, Job, Pin

POPULATE_DIR = 'atlascope/core/management/populate/'

MODEL_JSON_MAPPING = [
    (Dataset, 'datasets.json'),
    (Investigation, 'investigations.json'),
    (DatasetEmbedding, 'embeddings.json'),
    (Job, 'jobs.json'),
    (Pin, 'pins.json'),
]


def expand_references(obj, model):
    many_to_many_values = {}
    files_to_save = {}
    for field_name, value in obj.items():
        found_field = [field for field in model._meta.fields if field.name == field_name]
        found_field = found_field[0] if len(found_field) > 0 else None
        if hasattr(found_field, 'remote_field') and hasattr(found_field.remote_field, 'model'):
            remote_model = found_field.remote_field.model
            obj[field_name] = remote_model.objects.get(name=value)
        elif hasattr(found_field, 'upload_to'):
            target_file = open(Path(POPULATE_DIR, 'inputs', value), 'rb')
            files_to_save[field_name] = {
                'name': value,
                'contents': target_file,
            }
        elif isinstance(found_field, PolygonField):
            obj[field_name] = Polygon.from_bbox(tuple(value))
        elif isinstance(found_field, PointField):
            obj[field_name] = Point((value['x'], value['y']))
        found_many_to_many = [
            field for field in model._meta.many_to_many if field.name == field_name
        ]
        found_many_to_many = found_many_to_many[0] if len(found_many_to_many) > 0 else None
        if found_many_to_many:
            remote_model = found_many_to_many.remote_field.model
            if remote_model == Dataset:
                many_to_many_values[field_name] = [remote_model.objects.get(name=x) for x in value]
    for field_name in many_to_many_values.keys():
        del obj[field_name]
    return obj, many_to_many_values, files_to_save


@click.command()
def command():
    # delete in reverse order because of dependency protections
    for model, _ in reversed(MODEL_JSON_MAPPING):
        if model == Dataset:
            model.objects.filter(source_dataset__isnull=False).delete()
        model.objects.all().delete()
        print(f'Deleted all existing {model.__name__}s.')
    for model, filename in MODEL_JSON_MAPPING:
        print('-----')
        objects = json.load(open(POPULATE_DIR + filename))
        for obj in objects:
            if 'kwargs' in obj:
                kwargs = obj['kwargs']
                del obj['kwargs']
                if 'content' in kwargs:
                    obj['content'] = kwargs['content']
                    del kwargs['content']
            obj, many_to_many_values, files_to_save = expand_references(obj, model)
            db_obj = model(**obj)
            db_obj.save()
            identifier = list(obj.values())[0]
            if type(identifier) != str:
                identifier = str(db_obj)
            print(f'Saved {model.__name__}: {identifier}')

            for field_name, relations in many_to_many_values.items():
                getattr(db_obj, field_name).set(relations)
            for field_name, file_to_save in files_to_save.items():
                getattr(db_obj, field_name).save(file_to_save['name'], file_to_save['contents'])
            db_obj.save()

            if model == Job:
                db_obj.spawn()
                print('Successfully spawned job run!')
            if model == Dataset and not db_obj.content:
                print("  performing import...")
                try:
                    db_obj.perform_import(**kwargs)
                except ValidationError as e:
                    if 'DJANGO_API_TOKEN' not in os.environ:
                        print('    ! DJANGO_API_TOKEN not set in environment.')
                        print('    ! Skipping import for {db_obj.name}.')
                    else:
                        raise e
                print("  import complete!")

    print('-----')
    print('Dataload complete.')
