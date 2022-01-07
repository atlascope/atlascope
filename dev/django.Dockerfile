FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system libraries for Python packages
RUN apt-get update \
 && apt-get install --no-install-recommends --yes \
        # compilers
        gcc g++ binutils libc6-dev \
        # python
        python-is-python3 python3-dev python3-pip \
        # PostgreSQL library development files (psycopg2)
        libpq-dev \
        # gdal development files and binary (GeoDjango, large_image[gdal])
        libgdal-dev gdal-bin gdal-data \
        # proj development files and binary (GeoDjango, large_image[gdal])
        libproj-dev proj-bin proj-data \
        # geos library development files (GeoDjango)
        libgeos-dev \
 && rm -rf /var/lib/apt/lists/*


# Only copy the setup.py, it will still force all install_requires to be installed,
# but find_packages() will find nothing (which is fine). When Docker Compose mounts the real source
# over top of this directory, the .egg-link in site-packages resolves to the mounted directory
# and all package modules are importable.
COPY ./setup.py /opt/django-project/setup.py
RUN pip install \
        --editable '/opt/django-project[dev]' \
        # constrain GDAL for use with Ubuntu Focal library version
        'gdal==3.0.4' \
        # constrain pyproj for use with Ubuntu Focal library version
        'pyproj~=2.0'

# Use a directory name which will never be an import name, as isort considers this as first-party.
WORKDIR /opt/django-project

COPY atlascope_plugins /opt/atlascope-plugins/
RUN pip install --editable /opt/atlascope-plugins/*
