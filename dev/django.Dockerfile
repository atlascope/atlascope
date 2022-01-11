FROM ubuntu:20.04

# Install system libraries for Python packages:
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --yes \
        # C compilers and C standard library development files
        gcc libc6-dev \
        # Python
        python-is-python3 python3-dev python3-pip \
        # PostgreSQL library development files (psycopg2)
        libpq-dev \
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
RUN pip install --editable /opt/django-project[dev]

COPY ./atlascope_plugins/atlascope-vandy-importer/setup.py /opt/atlascope-plugins/atlascope-vandy-importer/setup.py
RUN pip install --editable /opt/atlascope-plugins/atlascope-vandy-importer

# Use a directory name which will never be an import name, as isort considers this as first-party.
WORKDIR /opt/django-project

# Setup nginx to proxy localhost:9000 to minio:9000
COPY ./dev/nginx.conf /etc/nginx/nginx.conf
COPY ./dev/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
