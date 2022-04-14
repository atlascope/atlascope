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
from configurations import values


class AtlascopeMixin(ConfigMixin):
    WSGI_APPLICATION = 'atlascope.wsgi.application'
    ROOT_URLCONF = 'atlascope.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    MEDIA_ROOT = BASE_DIR / Path('data')
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    # custom Atlascope definitions
    DATASET_TYPES = [
        'tile_source',
        'tile_overlay',
        'analytics',
        'subimage',
        'non_tiled_image',
    ]

    # Use PostGIS
    DATABASES = values.DatabaseURLValue(
        environ_name='DATABASE_URL',
        # django-configurations has environ_prefix=None by default here
        environ_prefix='DJANGO',
        environ_required=True,
        # Additional kwargs to DatabaseURLValue are passed to dj-database-url,
        # then passed through to the Django database options.
        engine='django.contrib.gis.db.backends.postgis',
        conn_max_age=600,
    )

    @staticmethod
    def mutate_configuration(configuration: ComposedConfiguration) -> None:
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            'atlascope.core.apps.CoreConfig',
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += [
            'django.contrib.gis',
        ]

        # Allow CORS requests to use credentials. Necessary for geojs on the client
        configuration.CORS_ALLOW_CREDENTIALS = True

        # Remove permission controls
        drf_config = configuration.REST_FRAMEWORK
        drf_config['DEFAULT_PERMISSION_CLASSES'] = []


class DevelopmentConfiguration(AtlascopeMixin, DevelopmentBaseConfiguration):
    pass


class TestingConfiguration(AtlascopeMixin, TestingBaseConfiguration):
    pass


class ProductionConfiguration(AtlascopeMixin, ProductionBaseConfiguration):
    pass


class HerokuProductionConfiguration(AtlascopeMixin, HerokuProductionBaseConfiguration):
    # Use PostGIS
    DATABASES = values.DatabaseURLValue(
        environ_name='DATABASE_URL',
        environ_prefix=None,
        environ_required=True,
        # Additional kwargs here.
        engine='django.contrib.gis.db.backends.postgis',
        conn_max_age=600,
        # Heroku is expected to always provide SSL.
        ssl_require=True,
    )
