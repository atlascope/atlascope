from importlib_metadata import entry_points

discovered_importer_plugins = entry_points(group='atlascope.plugins')
importers = {importer.name: importer.load() for importer in discovered_importer_plugins}
