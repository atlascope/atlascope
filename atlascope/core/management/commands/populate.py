import json
import os
from pathlib import Path

from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
import djclick as click
from guardian.shortcuts import assign_perm
from oauth2_provider.models import Application
from rest_framework.serializers import ValidationError

from atlascope.core.models import Dataset, DatasetEmbedding, Investigation, Job

POPULATE_DIR = 'atlascope/core/management/populate/'

MODEL_JSON_MAPPING = [
    (User, 'users.json'),
    (Dataset, 'datasets.json'),
    (Investigation, 'investigations.json'),
    (DatasetEmbedding, 'embeddings.json'),
    (Job, 'jobs.json'),
]

DEFAULT_PASSWORD = 'letmein'

DEFAULT_CLIENT_URI = 'http://localhost:8080/'


def expand_references(obj, model):
    many_to_many_values = {}
    files_to_save = {}
    permissions = {}
    for field_name, value in obj.items():
        found_field = [field for field in model._meta.fields if field.name == field_name]
        found_field = found_field[0] if len(found_field) > 0 else None
        if hasattr(found_field, 'remote_field') and hasattr(found_field.remote_field, 'model'):
            remote_model = found_field.remote_field.model
            if remote_model == User:
                obj[field_name] = remote_model.objects.get(email=value)
            else:
                obj[field_name] = remote_model.objects.get(name=value)
        elif hasattr(found_field, 'upload_to'):
            target_file = open(Path(POPULATE_DIR, 'inputs', value), 'rb')
            files_to_save[field_name] = {
                'name': value,
                'contents': target_file,
            }
        elif isinstance(found_field, PointField):
            obj[field_name] = Point(*value)
        found_many_to_many = [
            field for field in model._meta.many_to_many if field.name == field_name
        ]
        found_many_to_many = found_many_to_many[0] if len(found_many_to_many) > 0 else None
        if found_many_to_many:
            remote_model = found_many_to_many.remote_field.model
            if remote_model == Dataset:
                many_to_many_values[field_name] = [remote_model.objects.get(name=x) for x in value]
            elif remote_model == User:
                many_to_many_values[field_name] = [remote_model.objects.get(email=x) for x in value]
    for field_name in many_to_many_values.keys():
        del obj[field_name]
    for field_name, permission in {
        'investigators': 'change_investigation',
        'observers': 'view_investigation',
    }.items():
        if field_name in obj:
            permissions[permission] = [
                User.objects.get(username=username) for username in obj[field_name]
            ]
            del obj[field_name]
    return obj, many_to_many_values, files_to_save, permissions


@click.option('--password', type=click.STRING, help='password to apply to all users')
@click.command()
def command(password):
    Application.objects.get_or_create(
        client_id='cBmD6D6F2YAmMWHNQZFPUr4OpaXVpW5w4Thod6Kj',
        client_type='public',
        redirect_uris=DEFAULT_CLIENT_URI,
        authorization_grant_type='authorization-code',
        skip_authorization=True,
    )
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
            obj, many_to_many_values, files_to_save, permissions = expand_references(obj, model)
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
            for perm, user_list in permissions.items():
                [assign_perm(perm, user, db_obj) for user in user_list]
            db_obj.save()

            if model == User:
                db_obj.set_password(password or DEFAULT_PASSWORD)
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
