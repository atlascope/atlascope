import json
import os
from pathlib import Path

from django.contrib.gis.geos import Point
from django.contrib.gis.geos.polygon import Polygon
import djclick as click
from jsonschema import validate
from rest_framework.serializers import ValidationError

from atlascope.core.models import (
    Dataset,
    DatasetEmbedding,
    Investigation,
    Job,
    Pin,
    NotePin,
    DatasetPin,
    Tour,
    TourWaypoints,
    Waypoint,
)

POPULATE_DIR = Path('atlascope/core/management/populate/')

spec_types = ["datasets", "investigations", "embeddings", "jobs", "pins", "tours"]


def validate_all(spec):
    schema = get_json(POPULATE_DIR / "schema.json")

    for s in spec_types:
        print(f"Validating {s}.json...", end="", flush=True)
        validate(instance=spec[s], schema=schema[s])
        print("done")


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
    # Delete dataset objects in reverse order of source dataset references
    print("  Dataset objects...", end="", flush=True)
    while Dataset.objects.count() > 0:
        Dataset.objects.filter(derived_datasets=None).delete()
    print("done")

    # Delete the other objects. Go in reverse order of model creation.
    for model in [Investigation, DatasetEmbedding, Job, Pin, Waypoint, Tour]:
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
        spec["location"] = Point(spec["location"])
        if "child" in spec:
            print(f"""  Pin '{spec["parent"].name}' ({spec["investigation"].name})""")
            spec["child"] = Dataset.objects.get(name=spec["child"])
            pin = DatasetPin(**spec)
            pin.save()
        elif "note" in spec:
            print(f"""  Pin '{spec["parent"].name}' ({spec["investigation"].name})""")
            pin = NotePin(**spec)
            pin.save()


@announce("Populating tours")
def populate_tours(specs):
    for spec in specs:
        spec["investigation"] = Investigation.objects.get(name=spec["investigation"])
        waypoints = spec["waypoints"]
        del spec["waypoints"]

        # Build and save the Tour object.
        print(f"""  Tour '{spec["name"]}' """)
        tour = Tour(**spec)
        tour.save()

        # Build and save the Waypoint objects
        for s, w in enumerate(waypoints):
            w["location"] = Point(w["location"])
            waypoint = Waypoint(**w)
            waypoint.save()

            tw = TourWaypoints(sequence=s, tour=tour, waypoint=waypoint)
            tw.save()


def get_json(jsonfile):
    return json.load(open(jsonfile))


@click.command()
def command():
    spec = {}
    for s in spec_types:
        spec[s] = get_json(POPULATE_DIR / f"{s}.json")

    validate_all(spec)

    delete_all()

    populate_datasets(spec['datasets'])
    populate_investigations(spec['investigations'])
    populate_embeddings(spec['embeddings'])
    populate_jobs(spec['jobs'])
    populate_pins(spec['pins'])
    populate_tours(spec['tours'])
