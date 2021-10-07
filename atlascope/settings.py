from __future__ import annotations

from pathlib import Path

from composed_configuration import (
    ComposedConfiguration,
    ConfigMixin,
    DevelopmentBaseConfiguration,
    HerokuProductionBaseConfiguration,
    ProductionBaseConfiguration,
    TestingBaseConfiguration,
)


class AtlascopeMixin(ConfigMixin):
    WSGI_APPLICATION = 'atlascope.wsgi.application'
    ROOT_URLCONF = 'atlascope.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    @staticmethod
    def mutate_configuration(configuration: ComposedConfiguration) -> None:
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            'atlascope.core.apps.CoreConfig',
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += [
            's3_file_field',
        ]


class DevelopmentConfiguration(AtlascopeMixin, DevelopmentBaseConfiguration):
    pass


class TestingConfiguration(AtlascopeMixin, TestingBaseConfiguration):
    pass


class ProductionConfiguration(AtlascopeMixin, ProductionBaseConfiguration):
    pass


class HerokuProductionConfiguration(AtlascopeMixin, HerokuProductionBaseConfiguration):
    pass
