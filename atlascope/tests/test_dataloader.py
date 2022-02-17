import json
from typing import Iterator, Tuple

from django.contrib.auth.models import User
import pytest
from rest_framework import serializers

from atlascope.core import models as atlascope_models
from atlascope.core.management.commands.populate import DATALOADER_DIR, MODEL_JSON_MAPPING
from atlascope.core.rest.additional_serializers import UserSerializer


def serializer_dataloader_objects() -> Iterator[Tuple[serializers.ModelSerializer, dict]]:
    model_serializers = {
        clas.Meta.model: clas
        for clas in atlascope_models.__all__
        if issubclass(clas, serializers.ModelSerializer)
    }
    model_serializers[User] = UserSerializer
    for model, filename in MODEL_JSON_MAPPING:
        serializer = model_serializers[model]
        with open(DATALOADER_DIR + filename, 'r') as dataloader_file:
            dataloader_objects = json.load(dataloader_file)
            for dataloader_object in dataloader_objects:
                yield serializer, dataloader_object


@pytest.mark.django_db
@pytest.mark.parametrize("serializer,data_obj", serializer_dataloader_objects())
def test_serializers_valid(serializer, data_obj):
    serializer(data=data_obj).is_valid(raise_exception=True)
