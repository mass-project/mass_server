from mass_flask_core.models import DBSchemaVersion

class SchemaMigration:
    def __init__(self, db_schema_version):
        if not isinstance(db_schema_version, DBSchemaVersion):
            return
        self.db_schema_version = db_schema_version

    def update_schema():
        pass
