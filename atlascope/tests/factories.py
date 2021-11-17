from django.contrib.auth.models import User
import factory

from atlascope.core.models import ConnectionsMap, ContextMap, Dataset, Investigation, Pin


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
    color = factory.fuzzy.FuzzyChoice(Pin.color.choices, getter=lambda c: c[0])
    note = factory.Faker('sentence')
    dataset = factory.SubFactory(DatasetFactory)


class ContextMapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContextMap

    id = factory.Faker('uuid4')


class ConnectionsMapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ConnectionsMap

    id = factory.Faker('uuid4')
    notes = factory.Faker('sentence')


class InvestigationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Investigation

    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    owner = factory.SubFactory(UserFactory)
    context_map = factory.SubFactory(ContextMapFactory)
    connections_map = factory.SubFactory(ConnectionsMapFactory)
