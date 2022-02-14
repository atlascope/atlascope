from inspect import Parameter, signature

import pytest

from atlascope.core import models
from atlascope.core.job_types import available_job_types
from atlascope.core.rest.additional_serializers import UserSerializer
from atlascope.core.rest.permissions import has_read_perm

# ------------------------------------------------------------------
# USER ENDPOINT TESTS


@pytest.mark.django_db
def test_list_users(least_perm_api_client, user, user_factory):
    users = [user_factory() for i in range(3)] + [user]
    users.sort(key=lambda u: u.username)
    expected_results = [UserSerializer(u).data for u in users]
    resp = least_perm_api_client().get('/api/v1/users')
    assert resp.status_code == 200
    assert resp.json()['results'] == expected_results
    assert resp.json() == {
        'count': len(expected_results),
        'next': None,
        'previous': None,
        'results': expected_results,
    }


@pytest.mark.django_db
def test_retrieve_user(least_perm_api_client, user_factory):
    target_user = user_factory()
    resp = least_perm_api_client().get(f'/api/v1/users/{target_user.id}')
    assert resp.status_code == 200
    assert resp.json() == {
        'first_name': target_user.first_name,
        'last_name': target_user.last_name,
        'id': target_user.id,
        'username': target_user.username,
        'email': target_user.email,
    }


@pytest.mark.django_db
def test_retrieve_me(least_perm_api_client, user):
    resp = least_perm_api_client().get('/api/v1/users/me')
    assert resp.status_code == 200
    assert resp.json() == {
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
    investigations = [investigation_factory() for i in range(3)]
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
    assert resp.json() == {
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
        assert resp.json() == models.InvestigationDetailSerializer(investigation).data
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
    assert resp.json() == new_permissions


@pytest.mark.django_db
def test_get_investigation_pins(user_api_client, user, investigation, pin_factory):
    pin_set = [pin_factory() for i in range(5)]
    investigation.pins.set(pin_set)
    resp = user_api_client(investigation=investigation).get(
        f'/api/v1/investigations/{investigation.id}/pins'
    )
    if has_read_perm(user, investigation):
        assert resp.status_code == 200
        assert resp.json() == [models.PinSerializer(pin).data for pin in pin_set]
    else:
        assert resp.status_code == 404


# ------------------------------------------------------------------
# DATASET ENDPOINT TESTS


@pytest.mark.django_db
def test_list_datasets(user_api_client, user, dataset_factory):
    datasets = [dataset_factory() for i in range(3)]
    datasets.sort(key=lambda d: d.name)
    user_api_client = user_api_client(dataset=datasets[0])
    expected_results = [
        models.DatasetSerializer(d).data
        for d in datasets
        if (d.public or user.is_superuser or (has_read_perm(user, d)))
    ]
    resp = user_api_client.get('/api/v1/datasets')

    assert resp.status_code == 200
    assert resp.json() == {
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
    assert resp_public.data == models.DatasetSerializer(dataset_public).data

    resp_private = user_api_client(dataset=dataset_private).get(
        f'/api/v1/datasets/{dataset_private.id}'
    )
    if has_read_perm(user, dataset_private):
        assert resp_private.status_code == 200
        assert resp_private.data == models.DatasetSerializer(dataset_private).data
    else:
        assert resp_private.status_code == 404


# ------------------------------------------------------------------
# JOB ENDPOINT TESTS


@pytest.mark.django_db
def test_list_jobs(least_perm_api_client, job_factory):
    jobs = [job_factory() for i in range(1)]
    jobs.sort(key=lambda jr: str(jr.id))
    expected_results = [models.JobSerializer(job).data for job in jobs]
    resp = least_perm_api_client().get('/api/v1/jobs')
    assert resp.status_code == 200
    assert resp.json() == {
        'count': len(expected_results),
        'next': None,
        'previous': None,
        'results': expected_results,
    }


@pytest.mark.django_db
def test_retrieve_job(least_perm_api_client, job):
    resp = least_perm_api_client().get(f'/api/v1/jobs/{job.id}')
    assert resp.status_code == 200
    assert resp.json() == models.JobSerializer(job).data


@pytest.mark.django_db
def test_spawn_job(least_perm_api_client, job, dataset):
    serializer = models.JobSerializer(job)
    resp = least_perm_api_client().post('/api/v1/jobs', data=serializer.data)
    assert resp.status_code == 201


@pytest.mark.django_db
def test_rerun_job(least_perm_api_client, job):
    resp = least_perm_api_client().post(f'/api/v1/jobs/{job.id}/rerun')
    assert resp.status_code == 204


@pytest.mark.django_db
def test_list_job_types(least_perm_api_client):
    expected_results = {
        key: {
            'description': module.__doc__,
            'additional_inputs': [
                {
                    "name": name,
                    "class": param.annotation.__name__,
                    "required": param.default == Parameter.empty,
                }
                for name, param in signature(module).parameters.items()
                if name != 'original_dataset_id'
            ],
        }
        for key, module in available_job_types.items()
    }
    resp = least_perm_api_client().get('/api/v1/jobs/types')
    assert resp.status_code == 200
    assert resp.json() == expected_results
