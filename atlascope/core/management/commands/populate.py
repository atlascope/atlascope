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


def populate_datasets(specs):
    print("Populating Datasets...")

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


def populate_investigations(specs):
    print("Populating Investigations...")

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


def populate_embeddings(specs):
    print("Populating dataset embeddings...")

    for spec in specs:
        # Replace the names in the spec with the models they reference.
        spec["investigation"] = Investigation.objects.get(name=spec["investigation"])
        spec["parent"] = Dataset.objects.get(name=spec["parent"])
        spec["child"] = Dataset.objects.get(name=spec["child"])
        spec["child_bounding_box"] = Polygon.from_bbox(tuple(spec["child_bounding_box"]))

        # Build and save the DatasetEmbedding object.
        print(f"""  DatasetEmbedding '{spec["child"].name}' -> '{spec["parent"].name}' ({spec["investigation"].name})""")
        embedding = DatasetEmbedding(**spec)
        embedding.save()

    print("")


def populate_jobs(specs):
    print("Populating jobs...")

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

    print("")


def populate_pins(specs):
    print("Populating pins...")

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

    print("")


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
