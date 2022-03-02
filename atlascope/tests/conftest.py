from pathlib import Path

from django.core.files import File
from guardian.shortcuts import assign_perm
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from s3_file_field_client import S3FileFieldClient

from atlascope.core.management.commands.populate import POPULATE_DIR
from atlascope.tests import factories

register(factories.InvestigationFactory)
register(factories.DatasetFactory)
register(factories.PinFactory)
register(factories.JobFactory)


@pytest.fixture()
def user_api_client(request) -> APIClient:
    def _method(**kwargs):
        api_client = APIClient()
        return api_client

    return _method


@pytest.fixture()
def least_perm_api_client(request) -> APIClient:
    def _method(**kwargs):
        api_client = APIClient()
        return api_client

    return _method


@pytest.fixture()
def green_cell_upload(s3ff_field_value_factory) -> S3FileFieldClient:
    file_name = Path(POPULATE_DIR, 'inputs', 'green_cell_dataset_selection.png')
    stored_file = File(open(file_name, 'rb'))
    s3ff_field_value = s3ff_field_value_factory(stored_file)
    return s3ff_field_value
