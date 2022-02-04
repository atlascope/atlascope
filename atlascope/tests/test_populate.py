import os
import pytest
from atlascope.core.management.commands.populate import command as populate_command


@pytest.mark.django_db
def test_populate_script():
    populate_command()
