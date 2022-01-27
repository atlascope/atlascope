from inspect import signature


class AtlascopeImporter:
    def get_schema(self):
        return signature(self.perform_import)

    def perform_import(self):
        pass
