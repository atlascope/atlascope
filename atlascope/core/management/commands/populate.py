import json
import os
from pathlib import Path

from django.contrib.gis.db.models import PointField, PolygonField
from django.contrib.gis.geos import Point
from django.contrib.gis.geos.polygon import Polygon
import djclick as click
from rest_framework.serializers import ValidationError

from atlascope.core.models import Dataset, DatasetEmbedding, Investigation, Job, Pin

POPULATE_DIR = Path('atlascope/core/management/populate/')

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
            target_file = open(POPULATE_DIR / 'inputs' / value, 'rb')
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


def delete_all():
    print("Deleting...")

    # Delete dataset objects.
    print("  Dataset objects...", end="", flush=True)
    Dataset.objects.filter(source_dataset__isnull=False).delete()
    Dataset.objects.all().delete()
    print("done")

    # Delete the other objects. Go in reverse order of model creation.
    for Model in [Investigation, DatasetEmbedding, Job, Pin]:
        print(f"  {Model.__name__} objects...", end="", flush=True)
        Model.objects.all().delete()
        print("done")

    print("")


def populate_datasets(jsonfile):
    print("Populating Datasets...")

    # Read in the spec.
    specs = json.load(open(jsonfile))

    for spec in specs:
        # Separate any importer arguments.
        importer = spec.get("importer")
        if importer:
            del spec["importer"]

        # Grab any file to upload.
        content = spec.get("content")
        if content:
            del spec["content"]

        # Build and save the dataset object.
        print(f"""  Dataset '{spec["name"]}'""")
        dataset = Dataset(**spec)
        dataset.save()

        # If there's content to save, save it.
        if content:
            print("    uploading data...", end="", flush=True)
            dataset.content.save(content, open(POPULATE_DIR / "inputs" / content, "rb"))
            print("done")

        # If there's an importer to run, run it.
        if importer:
            print("    running importer...", end="", flush=True)
            try:
                dataset.perform_import(**importer)
                print("done")
            except ValidationError:
                if 'DJANGO_API_TOKEN' not in os.environ:
                    print("skipped (DJANGO_API_TOKEN not set)")
                else:
                    raise

    print("")


def populate_investigations(jsonfile):
    print("Populating Investigations...")

    # Read in the spec.
    specs = json.load(open(jsonfile))

    for spec in specs:
        # Pull out the dataset models that are in the investigation.
        datasets = [Dataset.objects.get(name=name) for name in spec["datasets"]]
        del spec["datasets"]

        # Build and save investigation objects.
        print(f"""  Investigation '{spec["name"]}'""")
        investigation = Investigation(**spec)
        investigation.save()

        # Associate the datasets to the investigation.
        print("    datasets:")
        for d in datasets:
            print(f"      {d.name}")
        investigation.datasets.set(datasets)

    print("")


@click.command()
def command():
    delete_all()

    populate_datasets(POPULATE_DIR / 'datasets.json')
    populate_investigations(POPULATE_DIR / 'investigations.json')

    for model, filename in MODEL_JSON_MAPPING[2:]:
        print('-----')
        objects = json.load(open(POPULATE_DIR / filename))
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
