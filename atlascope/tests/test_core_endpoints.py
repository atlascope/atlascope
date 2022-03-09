from inspect import Parameter, signature

import pytest

from atlascope.core import models
from atlascope.core.job_types import available_job_types

# ------------------------------------------------------------------
# INVESTIGATION ENDPOINT TESTS


@pytest.mark.django_db
def test_list_investigations(api_client, investigation_factory):
    investigations = [investigation_factory() for i in range(3)]
    investigations.sort(key=lambda i: i.name)
    api_client = api_client(investigation=investigations[0])
    expected_results = [models.InvestigationSerializer(i).data for i in (investigations)]
    resp = api_client.get('/api/v1/investigations')
    assert resp.status_code == 200
    assert resp.json() == {
        'count': len(expected_results),
        'next': None,
        'previous': None,
        'results': expected_results,
    }


@pytest.mark.django_db
def test_retrieve_investigation(api_client, investigation_factory):
    investigation = investigation_factory()
    resp = api_client().get(f'/api/v1/investigations/{investigation.id}')
    assert resp.status_code == 200
    assert resp.json() == models.InvestigationSerializer(investigation).data


@pytest.mark.django_db
def test_get_investigation_pins(api_client, investigation, pin_factory):
    pin_set = [pin_factory() for i in range(5)]
    investigation.pins.set(pin_set)
    resp = api_client(investigation=investigation).get(
        f'/api/v1/investigations/{investigation.id}/pins'
    )
    assert resp.status_code == 200
    assert resp.json() == [models.PinSerializer(pin).data for pin in pin_set]


# ------------------------------------------------------------------
# DATASET ENDPOINT TESTS


@pytest.mark.django_db
def test_list_datasets(api_client, dataset_factory):
    datasets = [dataset_factory() for i in range(3)]
    datasets.sort(key=lambda d: d.name)
    api_client = api_client(dataset=datasets[0])
    expected_results = [models.DatasetSerializer(d).data for d in datasets]
    resp = api_client.get('/api/v1/datasets')

    assert resp.status_code == 200
    assert resp.json() == {
        'count': len(expected_results),
        'next': None,
        'previous': None,
        'results': expected_results,
    }


@pytest.mark.django_db
def test_retrieve_dataset(api_client, dataset_factory):
    dataset = dataset_factory()

    resp = api_client(dataset=dataset).get(f'/api/v1/datasets/{dataset.id}')
    assert resp.status_code == 200
    assert resp.data == models.DatasetSerializer(dataset).data


@pytest.mark.django_db
def test_subimage(api_client, dataset_factory):
    test_data = {"original_dataset_id": dataset_factory().id, "x0": 1, "x1": 2, "y0": 3, "y1": 4}
    resp = api_client().post('/api/v1/datasets/subimage', data=test_data)
    assert resp.status_code == 201


# ------------------------------------------------------------------
# JOB ENDPOINT TESTS


@pytest.mark.django_db
def test_list_jobs(api_client, job_factory):
    jobs = [job_factory() for i in range(3)]
    jobs.sort(key=lambda d: d.id)
    expected_results = [models.JobDetailSerializer(job).data for job in jobs]
    resp = api_client().get('/api/v1/jobs')
    assert resp.status_code == 200
    assert resp.json() == {
        'count': len(expected_results),
        'next': None,
        'previous': None,
        'results': expected_results,
    }


@pytest.mark.django_db
def test_list_jobs_in_investigation(api_client, job_factory, investigation):
    jobs = [job_factory(investigation=investigation) for i in range(2)]
    [job_factory() for i in range(3)]  # make some unrelated jobs that should not be returned
    expected_results = [models.JobDetailSerializer(job).data for job in jobs]
    resp = api_client().get(f'/api/v1/investigations/{investigation.id}/jobs')
    assert resp.status_code == 200
    assert resp.json() == expected_results


@pytest.mark.django_db
def test_retrieve_job(api_client, job):
    resp = api_client().get(f'/api/v1/jobs/{job.id}')
    assert resp.status_code == 200
    assert resp.json() == models.JobDetailSerializer(job).data


@pytest.mark.django_db
def test_spawn_job(api_client, job, dataset):
    serializer = models.JobSpawnSerializer(job)
    resp = api_client().post('/api/v1/jobs', data=serializer.data)
    assert resp.status_code == 201


@pytest.mark.django_db
def test_rerun_job(api_client, job):
    resp = api_client().post(f'/api/v1/jobs/{job.id}/rerun')
    assert resp.status_code == 204


@pytest.mark.django_db
def test_list_job_types(api_client):
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
    resp = api_client().get('/api/v1/jobs/types')
    assert resp.status_code == 200
    assert resp.json() == expected_results
