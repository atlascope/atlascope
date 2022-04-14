import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from atlascope.tests import factories

register(factories.InvestigationFactory)
register(factories.DatasetFactory)
register(factories.PinFactory)
register(factories.JobFactory)


@pytest.fixture()
def api_client(request) -> APIClient:
    def _method(**kwargs):
        return APIClient()

    return _method
