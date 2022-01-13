import json
import pytest
from rest_framework import serializers
from django.contrib.auth.models import User

from atlascope.core import models as atlascope_models
from atlascope.core.management.commands.populate import MODEL_JSON_MAPPING, DATALOADER_DIR
from atlascope.core.rest.additional_serializers import UserSerializer


@pytest.mark.django_db
def test_serializers_valid():
    model_serializers = {
        clas.Meta.model: clas
        for clas in atlascope_models.__all__
        if issubclass(clas, serializers.ModelSerializer)
    }
    model_serializers[User] = UserSerializer

    for model, filename in MODEL_JSON_MAPPING:
        objects = json.load(open(DATALOADER_DIR + filename))
        for data_obj in objects:
            model_serializers[model](data=data_obj).is_valid()
