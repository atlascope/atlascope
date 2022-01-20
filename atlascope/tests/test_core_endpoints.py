import pytest

from atlascope.core.models import DatasetSerializer, InvestigationDetailSerializer, PinSerializer
from atlascope.core.rest.permissions import has_read_perm

# ------------------------------------------------------------------
# USER ENDPOINT TESTS


@pytest.mark.django_db
def test_list_users(user_api_client, user, user_factory):
    users = [user_factory() for i in range(5)] + [user]
    users.sort(key=lambda u: u.username)
    expected_results = [
        {
            'id': int(u.id),
            'username': u.username,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
        }
        for u in users
    ]
    resp = user_api_client().get('/api/v1/users')
    assert resp.status_code == 200
    assert resp.data['results'] == expected_results
    assert resp.data == {
        'count': 6,
        'next': None,
        'previous': None,
        'results': expected_results,
    }


@pytest.mark.django_db
def test_retrieve_user(user_api_client, user_factory):
    target_user = user_factory()
    resp = user_api_client().get(f'/api/v1/users/{target_user.id}')
    assert resp.status_code == 200
    assert resp.data == {
        'first_name': target_user.first_name,
        'last_name': target_user.last_name,
        'id': target_user.id,
        'username': target_user.username,
        'email': target_user.email,
    }


@pytest.mark.django_db
def test_retrieve_me(user_api_client, user):
    resp = user_api_client().get('/api/v1/users/me')
    assert resp.status_code == 200
    assert resp.data == {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


# ------------------------------------------------------------------
# INVESTIGATION ENDPOINT TESTS


@pytest.mark.django_db
def test_list_investigations(user_api_client, user, investigation_factory):
    investigations = [investigation_factory() for i in range(5)]
    investigations.sort(key=lambda i: i.name)
    user_api_client = user_api_client(investigation=investigations[0])
    expected_results = [
        {
            'id': i.id,
            'name': i.name,
            'description': i.description,
            'owner': i.owner.username,
        }
        for i in (
            investigations
            if user.is_superuser
            else investigations[:1]
            if has_read_perm(user, investigations[0])
            else []
        )
    ]
    resp = user_api_client.get('/api/v1/investigations')
    assert resp.status_code == 200
    assert resp.data == {
        'count': len(expected_results),
        'next': None,
        'previous': None,
        'results': expected_results,
    }


@pytest.mark.django_db
def test_retrieve_investigation(user_api_client, user, user_factory, investigation_factory):
    investigation = investigation_factory(owner=user_factory())
    resp = user_api_client(investigation=investigation).get(
        f'/api/v1/investigations/{investigation.id}'
    )
    if has_read_perm(user, investigation):
        assert resp.status_code == 200
        assert resp.json() == InvestigationDetailSerializer(investigation).data
    else:
        assert resp.status_code == 404


@pytest.mark.django_db
def test_change_investigation_permissions(user_api_client, user, user_factory, investigation):
    new_permissions = {
        'owner': user.username,
        'investigators': [
            user_factory().username,
            user_factory().username,
        ],
        'observers': [
            user_factory().username,
            user_factory().username,
        ],
    }
    resp = user_api_client(investigation=investigation).post(
        f'/api/v1/investigations/{investigation.id}/permissions', data=new_permissions
    )
    assert resp.status_code == 200
    assert resp.data == new_permissions


@pytest.mark.django_db
def test_get_investigation_pins(user_api_client, user, investigation, pin_factory):
    pin_set = [pin_factory() for i in range(5)]
    investigation.pins.set(pin_set)
    resp = user_api_client(investigation=investigation).get(
        f'/api/v1/investigations/{investigation.id}/pins'
    )
    if has_read_perm(user, investigation):
        assert resp.status_code == 200
        assert resp.json() == {str(pin.id): PinSerializer(pin).data for pin in pin_set}
    else:
        assert resp.status_code == 404


# ------------------------------------------------------------------
# INVESTIGATION ENDPOINT TESTS


@pytest.mark.django_db
def test_list_datasets(user_api_client, user, dataset_factory):
    datasets = [dataset_factory() for i in range(5)]
    datasets.sort(key=lambda d: d.name)
    user_api_client = user_api_client(dataset=datasets[0])
    expected_results = [
        DatasetSerializer(d).data
        for d in datasets
        if (d.public or user.is_superuser or (has_read_perm(user, d)))
    ]
    resp = user_api_client.get('/api/v1/datasets')

    assert resp.status_code == 200
    assert resp.data == {
        'count': len(expected_results),
        'next': None,
        'previous': None,
        'results': expected_results,
    }


@pytest.mark.django_db
def test_retrieve_dataset(user_api_client, user, dataset_factory):
    dataset_public = dataset_factory(public=True)
    dataset_private = dataset_factory(public=False)

    resp_public = user_api_client(dataset=dataset_public).get(
        f'/api/v1/datasets/{dataset_public.id}'
    )
    assert resp_public.status_code == 200
    assert resp_public.data == DatasetSerializer(dataset_public).data

    resp_private = user_api_client(dataset=dataset_private).get(
        f'/api/v1/datasets/{dataset_private.id}'
    )
    if has_read_perm(user, dataset_private):
        assert resp_private.status_code == 200
        assert resp_private.data == DatasetSerializer(dataset_private).data
    else:
        assert resp_private.status_code == 404
