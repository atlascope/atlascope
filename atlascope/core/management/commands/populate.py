import json

from django.contrib.auth.models import User
import djclick as click
from guardian.shortcuts import assign_perm
from oauth2_provider.models import Application

from atlascope.core.models import Investigation

DATALOADER_DIR = 'atlascope/core/management/dataloader/'

MODEL_JSON_MAPPING = [
    (User, 'users.json'),
    (Investigation, 'investigations.json'),
]

DEFAULT_PASSWORD = '123'

DEFAULT_CLIENT_URI = 'http://localhost:8081/'


def expand_references(obj, model):
    many_to_many_values = {}
    permissions = {}
    for field_name, value in obj.items():
        found_field = [field for field in model._meta.fields if field.name == field_name]
        found_field = found_field[0] if len(found_field) > 0 else None
        if hasattr(found_field, 'remote_field') and hasattr(found_field.remote_field, 'model'):
            obj[field_name] = found_field.remote_field.model.objects.get(email=value)
        else:
            found_many_to_many = [
                field for field in model._meta.many_to_many if field.name == field_name
            ]
            found_many_to_many = found_many_to_many[0] if len(found_many_to_many) > 0 else None
            if found_many_to_many:
                many_to_many_values[field_name] = [
                    found_many_to_many.remote_field.model.objects.get(email=x) for x in value
                ]
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
    return obj, many_to_many_values, permissions


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
        model.objects.all().delete()
        print(f'Deleted all existing {model.__name__}s.')
    for model, filename in MODEL_JSON_MAPPING:
        print('-----')
        objects = json.load(open(DATALOADER_DIR + filename))
        for obj in objects:
            obj, many_to_many_values, permissions = expand_references(obj, model)
            db_obj = model(**obj)
            db_obj.save()
            print(f'Saved {model.__name__}: {list(obj.values())[0]}')
            for field_name, relations in many_to_many_values.items():
                getattr(db_obj, field_name).set(relations)
            for perm, user_list in permissions.items():
                [assign_perm(perm, user, db_obj) for user in user_list]
            if model == User:
                db_obj.set_password(password or DEFAULT_PASSWORD)
                print(f'Password set to "{password or DEFAULT_PASSWORD}".')
            db_obj.save()
    print('-----')
    print('Dataload complete.')
