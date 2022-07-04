# Selected cohorts for validation

The following cohorts were copied from ATLAS Demo instance. We only used them for testing the impact of privacy-preserving techniques over the cohort results.

- I   - Respiratory Tract Infection (EHDEN Use Case) [ATLAS Demo here](https://atlas-demo.ohdsi.org/#/cohortdefinition/1779684/generation)
- II  - Cardiovascular Events (EHDEN Use Case) [ATLAS Demo here](https://atlas-demo.ohdsi.org/#/cohortdefinition/1779685/generation)
- III - Death (EHDEN Use Case) [ATLAS Demo here](https://atlas-demo.ohdsi.org/#/cohortdefinition/1779680/generation)
- IV  - Venous Thromboembolism (EHDEN Use Case) [ATLAS Demo here](https://atlas-demo.ohdsi.org/#/cohortdefinition/1779686/generation)
- V   - Sepsis (EHDEN Use Case) [ATLAS Demo here](https://atlas-demo.ohdsi.org/#/cohortdefinition/1779682/generation)

## Notes

```
select * from final_cohort inner join person on final_cohort.person_id=person.person_id inner join observation on observation.person_id=person.person_id;
```