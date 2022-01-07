FROM python:3.8-slim
# Install system libraries for Python packages:
RUN apt-get update \
 && apt-get install --no-install-recommends --yes \
        # C compilers and C standard library development files
        gcc libc6-dev \
        # PostgreSQL library development files (psycopg2)
        libpq-dev \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Only copy the setup.py, it will still force all install_requires to be installed,
# but find_packages() will find nothing (which is fine). When Docker Compose mounts the real source
# over top of this directory, the .egg-link in site-packages resolves to the mounted directory
# and all package modules are importable.
COPY ./setup.py /opt/django-project/setup.py
RUN pip install --editable /opt/django-project[dev]

# Use a directory name which will never be an import name, as isort considers this as first-party.
WORKDIR /opt/django-project

COPY atlascope_plugins /opt/atlascope-plugins/
RUN pip install --editable /opt/atlascope-plugins/*
