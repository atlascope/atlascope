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
    source_uri = factory.Faker('file_path')


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
