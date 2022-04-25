import pytest

from atlascope.core.management.commands.populate import command as populate_command


@pytest.mark.django_db
def test_metadata(api_client):
    populate_command()
    resp = api_client().get('/api/v1/datasets/tile_source/2000/tiles/metadata')
    assert resp.status_code == 200
    # Make sure OMETIFF reader was used
    assert 'frames' in resp.json()['additional_metadata']
