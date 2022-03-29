import json
import os
from pathlib import Path
import tempfile
import large_image_converter
import logging

from django.contrib.gis.geos import Point
from django.contrib.gis.geos.polygon import Polygon
import djclick as click
from rest_framework.serializers import ValidationError

from atlascope.core.models import Dataset, DatasetEmbedding, Investigation, Job, Pin

POPULATE_DIR = Path('atlascope/core/management/populate/')
logging.disable('INFO')
logging.disable('WARNING')


def announce(msg):
    def decorator(f):
        def wrapped(*args, **kwargs):
            print(f"{msg}...")
            f(*args, **kwargs)
            print("")

        return wrapped

    return decorator


@announce("Deleting")
def delete_all():
    # Delete dataset objects.
    print("  Dataset objects...", end="", flush=True)
    Dataset.objects.filter(source_dataset__isnull=False).delete()
    Dataset.objects.all().delete()
    print("done")

    # Delete the other objects. Go in reverse order of model creation.
    for model in [Investigation, DatasetEmbedding, Job, Pin]:
        print(f"  {model.__name__} objects...", end="", flush=True)
        model.objects.all().delete()
        print("done")


@announce("Populating datasets")
def populate_datasets(specs):
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
            with tempfile.TemporaryDirectory() as tmpdirname:
                dest = Path(tmpdirname, 'gdal_conversion')
                with open(dest, 'wb') as fd:
                    fd.write(open(POPULATE_DIR / "inputs" / content, "rb").read())
                converted = large_image_converter.convert(str(dest))
                dataset.content.save(content, open(converted, 'rb'))
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


@announce("Populating investigations")
def populate_investigations(specs):
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


@announce("Populating dataset embeddings")
def populate_embeddings(specs):
    for spec in specs:
        # Replace the names in the spec with the models they reference.
        spec["investigation"] = Investigation.objects.get(name=spec["investigation"])
        spec["parent"] = Dataset.objects.get(name=spec["parent"])
        spec["child"] = Dataset.objects.get(name=spec["child"])
        spec["child_bounding_box"] = Polygon.from_bbox(tuple(spec["child_bounding_box"]))

        # Build and save the DatasetEmbedding object.
        child = spec["child"].name
        parent = spec["parent"].name
        investigation = spec["investigation"].name
        print(f"""  DatasetEmbedding '{child}' -> '{parent}' ({investigation})""")
        embedding = DatasetEmbedding(**spec)
        embedding.save()


@announce("Populating jobs")
def populate_jobs(specs):
    for spec in specs:
        # Pull in the investigation and dataset referenced in the job spec.
        spec["investigation"] = Investigation.objects.get(name=spec["investigation"])
        spec["original_dataset"] = Dataset.objects.get(name=spec["original_dataset"])

        # Build and save the Job object.
        print(f"""  Job '{spec["job_type"]}' ({spec["investigation"].name})""")
        job = Job(**spec)
        job.save()

        print("    spawning job run...", end="", flush=True)
        job.spawn()
        print("done")


@announce("Populating pins")
def populate_pins(specs):
    for spec in specs:
        # Pull in foreign models and other objects.
        spec["investigation"] = Investigation.objects.get(name=spec["investigation"])
        spec["parent"] = Dataset.objects.get(name=spec["parent"])
        if "child" in spec:
            spec["child"] = Dataset.objects.get(name=spec["child"])
        spec["child_location"] = Point(spec["child_location"])

        # Build and save the Pin object.
        print(f"""  Pin '{spec["parent"].name}' ({spec["investigation"].name})""")
        pin = Pin(**spec)
        pin.save()


def get_json(jsonfile):
    return json.load(open(jsonfile))


@click.command()
def command():
    delete_all()

    populate_datasets(get_json(POPULATE_DIR / 'datasets.json'))
    populate_investigations(get_json(POPULATE_DIR / 'investigations.json'))
    populate_embeddings(get_json(POPULATE_DIR / 'embeddings.json'))
    populate_jobs(get_json(POPULATE_DIR / 'jobs.json'))
    populate_pins(get_json(POPULATE_DIR / 'pins.json'))
