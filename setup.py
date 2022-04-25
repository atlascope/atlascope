from pathlib import Path

from setuptools import find_packages, setup

readme_file = Path(__file__).parent / 'README.md'
if readme_file.exists():
    with readme_file.open() as f:
        long_description = f.read()
else:
    # When this is first installed in development Docker, README.md is not available
    long_description = ''

setup(
    name='atlascope',
    version='0.1.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    keywords='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
    ],
    python_requires='>=3.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'celery',
        'django>=3.2,<4.0',
        'django-allauth',
        'django-configurations[database,email]',
        'django-extensions',
        'django-filter',
        'django-oauth-toolkit',
        'djangorestframework',
        'drf-yasg',
        'django-click',
        'importlib_metadata>=3.6',
        'jsonschema',
        'large-image[gdal,ometiff]>=1.14',
        'django-large-image>=0.5.0',
        # Production-only
        'django-composed-configuration[prod]>=0.18',
        'gunicorn',
        'numpy',
        'pillow',
        'requests',
        # manual override until https://github.com/girder/large_image/pull/799
        'pylibtiff',
        # pylibtiff depends on this but it is not listed in its dependencies
        'bitarray',
    ],
    extras_require={
        'dev': [
            'django-composed-configuration[dev]>=0.18',
            'django-debug-toolbar',
            'ipython',
            'tox',
        ]
    },
)
