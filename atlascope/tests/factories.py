from django.contrib.auth.models import User
import factory

from atlascope.core import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.SelfAttribute('email')
    email = factory.Faker('safe_email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class DatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Dataset

    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')
    public = factory.Faker('boolean')
    content = None
    metadata = {}
    dataset_type = 'tile_source'

    @factory.post_generation
    def derived_datasets(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of derived_datasets were passed in, use them
            for derived_dataset in extracted:
                self.derived_datasets.add(derived_dataset)


class PinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Pin

    id = factory.Faker('uuid4')
    note = factory.Faker('sentence')
    dataset = factory.SubFactory(DatasetFactory)


class InvestigationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Investigation

    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    owner = factory.SubFactory(UserFactory)
    # datasets
    # pins
    # connections
    notes = factory.Faker('sentence')


class JobScriptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.JobScript

    id = factory.Faker('uuid4')
    name = factory.Faker('word')


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Job

    id = factory.Faker('uuid4')
    script = factory.SubFactory(JobScriptFactory)
    input_image = factory.django.FileField(data=factory.Faker('binary', length=100))
    other_inputs = {}
