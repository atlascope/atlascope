# Atlascope Plugin: Custom Importer

## Development
Put this directory (plugin source code) inside your atlascope repo as the following: `atlascope/atlascope_plugins/[this-plugin]`. The docker configuration will handle the rest. This plugin is not included in the main repository; the `atlascope/atlascope_plugins/` folder is ignored by git.


## Production
When an Atlascope plugin is complete and ready for use in Atlascope, it should be uploaded to PyPI. Then, any installations of Atlascope that need this plugin may perform a `pip install` of the plugin (or include the PyPI dist name in `setup.py`) and its functionality will automatically be made available.
