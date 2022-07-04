from pathlib import Path

k_anonymity = 10 #default
l_diversity = 5 #default

basePath = Path(__file__).parent
cdmSchemaPath = (basePath / "../aux/OMOP_CDMv5.4_Field_Level.csv").resolve()
pluginsPath = (basePath / "plugins").resolve()