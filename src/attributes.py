keyAttributes = [
	("PERSON","person_id"),
	("OBSERVATION_PERIOD","person_id"),
	("VISIT_OCCURRENCE","person_id"),
	("VISIT_DETAIL","person_id"),
	("CONDITION_OCCURRENCE","person_id"),
	("DRUG_EXPOSURE","person_id"),
	("PROCEDURE_OCCURRENCE","person_id"),
	("DEVICE_EXPOSURE","person_id"),
	("MEASUREMENT","person_id"),
	("OBSERVATION","person_id"),
	("DEATH","person_id"),
	("SPECIMEN","person_id"),
	("EPISODE","person_id"),
	("VISIT_OCCURRENCE","visit_occurrence_id"),
	("VISIT_OCCURRENCE","preceding_visit_occurrence_id"),
]
sensitiveAttributes = [
	("VISIT_OCCURRENCE","visit_concept_id"),
	("VISIT_OCCURRENCE","visit_type_concept_id"),
	("VISIT_OCCURRENCE","visit_source_value"),
	("VISIT_OCCURRENCE","visit_source_concept_id"),
	("VISIT_OCCURRENCE","admitted_from_concept_id"),
	("VISIT_OCCURRENCE","admitted_from_source_value"),
	("VISIT_OCCURRENCE","discharged_to_concept_id"),
	("VISIT_OCCURRENCE","discharged_to_source_value"),
]
quasiIdentifiers = [
	("PERSON","gender_concept_id"),
	("PERSON","year_of_birth"),
	("PERSON","month_of_birth"),
	("PERSON","day_of_birth"),
	("PERSON","birth_datetime"),
	("PERSON","race_concept_id"),
	("PERSON","ethnicity_concept_id"),
	("PERSON","location_id"),
	("PERSON","provider_id"),
	("PERSON","care_site_id"),
	("PERSON","person_source_value"),
	("PERSON","gender_source_value"),
	("PERSON","gender_source_concept_id"),
	("PERSON","race_source_value"),
	("PERSON","race_source_concept_id"),
	("PERSON","ethnicity_source_value"),
	("PERSON","ethnicity_source_concept_id"),
	("OBSERVATION_PERIOD","observation_period_id"),
	("OBSERVATION_PERIOD","observation_period_start_date"),
	("OBSERVATION_PERIOD","observation_period_end_date"),
	("OBSERVATION_PERIOD","period_type_concept_id"),
	("VISIT_OCCURRENCE","visit_start_date"),
	("VISIT_OCCURRENCE","visit_start_datetime"),
	("VISIT_OCCURRENCE","visit_end_date"),
	("VISIT_OCCURRENCE","visit_end_datetime"),
	("VISIT_OCCURRENCE","provider_id"),
	("VISIT_OCCURRENCE","care_site_id"),

]
