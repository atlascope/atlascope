from atlascope.core.management.commands.populate import command as populate_command

import pytest


@pytest.mark.django_db
def test_metadata(api_client):
    populate_command()
    resp = api_client().get(f'/api/v1/datasets/tile_source/2000/tiles/metadata')
    assert resp.status_code == 200
