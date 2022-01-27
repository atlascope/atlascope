import sys, inspect

clsmembers = inspect.getmembers(sys.modules['atlascope.core.importers'], inspect.isclass)
importers = {module[0]: module[1] for module in clsmembers if module[0] != 'AtlascopeImporter'}
