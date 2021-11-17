from guardian.shortcuts import assign_perm
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from atlascope.core.models import Investigation
from atlascope.tests.factories import DatasetFactory, InvestigationFactory, PinFactory, UserFactory

register(UserFactory)
register(InvestigationFactory)
register(DatasetFactory)
register(PinFactory)


@pytest.fixture(params=[None, 'superuser'] + Investigation.get_read_permission_groups())
def user_api_client(request, user, project) -> APIClient:
    def _method(**kwargs):
        api_client = APIClient()
        api_client.force_authenticate(user=user)
        if request.param:
            if request.param == 'superuser':
                user.is_superuser = True
                user.save()
            elif 'project' in kwargs:
                assign_perm(request.param, user, kwargs['project'])
            else:
                assign_perm(request.param, user, project)
        return api_client

    return _method
