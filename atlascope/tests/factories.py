from django.contrib.auth.models import User
import factory

from atlascope.core.models import Dataset, Investigation, Pin


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.SelfAttribute('email')
    email = factory.Faker('safe_email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class DatasetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dataset

    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')
    source_uri = factory.Faker('file_path')
    public = factory.Faker('boolean')
    importer = factory.Faker('word')
    content = None
    dataset_type = 'tile_source'
    metadata = None

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
        model = Pin

    id = factory.Faker('uuid4')
    note = factory.Faker('sentence')
    dataset = factory.SubFactory(DatasetFactory)


class InvestigationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Investigation

    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    owner = factory.SubFactory(UserFactory)
    # datasets
    # pins
    # connections
    notes = factory.Faker('sentence')
