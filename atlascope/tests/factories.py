from django.contrib.gis.geos import Point
from atlascope.core.models import investigation
import factory

from atlascope.core import models


class DatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Dataset

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    content = None
    metadata = {}
    dataset_type = 'tile_source'

    @factory.post_generation
    def source_dataset(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.source_dataset = extracted


class InvestigationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Investigation

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    notes = factory.Faker('sentence')

    @factory.post_generation
    def datasets(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for dataset in extracted:
                self.datasets.add(dataset)


class PinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Pin

    investigation = factory.SubFactory(InvestigationFactory)
    parent = factory.SubFactory(DatasetFactory)
    location = Point(5, 5)
    color = 'red'


class NotePinFactory(PinFactory):
    class Meta:
        model = models.NotePin

    note = factory.Faker('sentence')


class DatasetPinFactory(PinFactory):
    class Meta:
        model = models.DatasetPin

    child = factory.SubFactory(DatasetFactory)


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Job

    complete = False
    investigation = factory.SubFactory(InvestigationFactory)
    original_dataset = factory.SubFactory(DatasetFactory)
    additional_inputs = {}
    job_type = 'average_color'

    @factory.post_generation
    def resulting_datasets(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # A list of groups were passed in, use them
            for resulting_dataset in extracted:
                self.resulting_datasets.add(resulting_dataset)
