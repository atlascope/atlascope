from inspect import signature


class AtlascopeImporter:
    def __init__(self):
        self.content = None
        self.metadata = None

    @classmethod
    def get_schema(self):
        return signature(self.perform_import)

    def raise_schema_exception(self):
        raise Exception(
            f"This importer function requires the following parameters: {self.get_schema()}"
        )

    def perform_import(self):
        pass
