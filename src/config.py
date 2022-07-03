from pathlib import Path

basePath = Path(__file__).parent
cdmSchemaPath = (basePath / "../aux/OMOP_CDMv5.4_Field_Level.csv").resolve()
pluginsPath = (basePath / "plugins").resolve()