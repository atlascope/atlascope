from guardian.shortcuts import assign_perm
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from atlascope.tests.factories import DatasetFactory, InvestigationFactory, PinFactory, UserFactory

register(UserFactory)
register(InvestigationFactory)
register(DatasetFactory)
register(PinFactory)


@pytest.fixture(params=[None, 'superuser', 'view_model', 'change_model'])
def user_api_client(request, user) -> APIClient:
    def _method(**kwargs):
        api_client = APIClient()
        api_client.force_authenticate(user=user)
        if request.param:
            if request.param == 'superuser':
                user.is_superuser = True
                user.save()
            elif 'investigation' in kwargs:
                assign_perm(
                    request.param.replace('model', 'investigation'), user, kwargs['investigation']
                )
            elif 'dataset' in kwargs:
                assign_perm(request.param.replace('model', 'dataset'), user, kwargs['dataset'])
        return api_client

    return _method
