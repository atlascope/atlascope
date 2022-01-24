from setuptools import setup

setup(
    name="atlascope-vandy-importer",
    packages=["atlascope_vandy_importer"],
    version="0.0.1",
    entry_points={
        "atlascope.plugins": "vandy = atlascope_vandy_importer.import_function:run",
    },
    install_requires=[
        "requests",
        'importlib; python_version == "2.6"',
    ],
)
