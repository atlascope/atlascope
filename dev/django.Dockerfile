FROM ubuntu:20.04

# Install system libraries for Python packages:
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --yes \
        # C/C++ compilers and C standard library development files
        gcc g++ binutils g++ libc6-dev \
        # Python
        python-is-python3 python3-dev python3-pip \
        # PostgreSQL library development files (psycopg2)
        libpq-dev \
        # GDAL development files and binary (GeoDjango)
        libgdal-dev gdal-bin gdal-data \
        # PROJ development files and binary (GeoDjango)
        libproj-dev proj-bin proj-data \
        # GEOS library development files (GeoDjango)
        libgeos-dev \
        # Nginx to proxy localhost
        nginx \
 && pip install --upgrade pip \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Only copy the setup.py, it will still force all install_requires to be installed,
# but find_packages() will find nothing (which is fine). When Docker Compose mounts the real source
# over top of this directory, the .egg-link in site-packages resolves to the mounted directory
# and all package modules are importable.
COPY ./setup.py /opt/django-project/setup.py
RUN pip install \
        --editable /opt/django-project[dev] \
        # constrain GDAL for use with Ubuntu Focal library version
        'gdal==3.0.4' \
        # constrain pyproj for use with Ubuntu Focal library version
        'pyproj~=2.0'

# Use a directory name which will never be an import name, as isort considers this as first-party.
WORKDIR /opt/django-project

# Setup nginx to proxy localhost:9000 to minio:9000
COPY ./dev/nginx.conf /etc/nginx/nginx.conf
COPY ./dev/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
