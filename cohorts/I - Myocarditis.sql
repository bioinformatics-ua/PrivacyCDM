-- Copied from ATLAS Demo
-- Used only for testing the impact of privacy-preserving techniques on the cohort results
-- URL: https://atlas-demo.ohdsi.org/#/cohortdefinition/1779643

CREATE TEMP TABLE Codesets  (codeset_id int NOT NULL,
  concept_id bigint NOT NULL
)
;

INSERT INTO Codesets (codeset_id, concept_id)
SELECT 1 as codeset_id, c.concept_id FROM (select distinct I.concept_id FROM
( 
  select concept_id from CONCEPT where concept_id in (314383,318072,4103844,4138837,4149568,4149913,4230954,4289908,36674262,44782774)
UNION  select c.concept_id
  from CONCEPT c
  join CONCEPT_ANCESTOR ca on c.concept_id = ca.descendant_concept_id
  and ca.ancestor_concept_id in (314383,318072,4103844,4138837,4149568,4149913,4230954,4289908,36674262,44782774)
  and c.invalid_reason is null

) I
LEFT JOIN
(
  select concept_id from CONCEPT where concept_id in (4068262,4185379,45766166,4225077,43020931,4147982,4258681,35207754,1569160,35207718,35207717,35207719,35207753,35207715,35207716,35207752,35207919,45581156,1569153,35207720,45571465,35207750,35207725,35207751,45463044,3119660,45509623,45547405,3321727,3418560,312543,44820547,40383314,319720,45566503,44832068)
UNION  select c.concept_id
  from CONCEPT c
  join CONCEPT_ANCESTOR ca on c.concept_id = ca.descendant_concept_id
  and ca.ancestor_concept_id in (4068262,4185379,45766166,4225077,43020931,4147982,4258681,35207754,1569160,35207718,35207717,35207719,35207753,35207715,35207716,35207752,35207919,45581156,1569153,35207720,45571465,35207750,35207725,35207751,45463044,3119660,45509623,45547405,3321727,3418560,312543,44820547,40383314,319720,45566503,44832068)
  and c.invalid_reason is null

) E ON I.concept_id = E.concept_id
WHERE E.concept_id is null
) C
;

CREATE TEMP TABLE qualified_events

AS
WITH primary_events (event_id, person_id, start_date, end_date, op_start_date, op_end_date, visit_occurrence_id)  AS (
-- Begin Primary Events
select P.ordinal as event_id, P.person_id, P.start_date, P.end_date, op_start_date, op_end_date, cast(P.visit_occurrence_id as bigint) as visit_occurrence_id
FROM
(
  select E.person_id, E.start_date, E.end_date,
         row_number() OVER (PARTITION BY E.person_id ORDER BY E.sort_date ASC) ordinal,
         OP.observation_period_start_date as op_start_date, OP.observation_period_end_date as op_end_date, cast(E.visit_occurrence_id as bigint) as visit_occurrence_id
  FROM 
  (
  -- Begin Condition Era Criteria
select C.person_id, C.condition_era_id as event_id, C.condition_era_start_date as start_date,
       C.condition_era_end_date as end_date, CAST(NULL as bigint) as visit_occurrence_id,
       C.condition_era_start_date as sort_date
from 
(
  select ce.* 
  FROM CONDITION_ERA ce
where ce.condition_concept_id in (SELECT concept_id from  Codesets where codeset_id = 1)
) C


-- End Condition Era Criteria

  ) E
	JOIN observation_period OP on E.person_id = OP.person_id and E.start_date >=  OP.observation_period_start_date and E.start_date <= op.observation_period_end_date
  WHERE (OP.OBSERVATION_PERIOD_START_DATE + 0*INTERVAL'1 day') <= E.START_DATE AND (E.START_DATE + 0*INTERVAL'1 day') <= OP.OBSERVATION_PERIOD_END_DATE
) P
WHERE P.ordinal = 1
-- End Primary Events

)
 SELECT
event_id, person_id, start_date, end_date, op_start_date, op_end_date, visit_occurrence_id

FROM
(
  select pe.event_id, pe.person_id, pe.start_date, pe.end_date, pe.op_start_date, pe.op_end_date, row_number() over (partition by pe.person_id order by pe.start_date ASC) as ordinal, cast(pe.visit_occurrence_id as bigint) as visit_occurrence_id
  FROM primary_events pe
  
) QE

;
ANALYZE qualified_events
;

--- Inclusion Rule Inserts

CREATE TEMP TABLE Inclusion_0

AS
SELECT
0 as inclusion_rule_id, person_id, event_id

FROM
(
  select pe.person_id, pe.event_id
  FROM qualified_events pe
  
JOIN (
-- Begin Criteria Group
select 0 as index_id, person_id, event_id
FROM
(
  select E.person_id, E.event_id 
  FROM qualified_events E
  INNER JOIN
  (
    -- Begin Correlated Criteria
select 0 as index_id, cc.person_id, cc.event_id
from (SELECT p.person_id, p.event_id 
FROM qualified_events P
JOIN (
  -- Begin Condition Era Criteria
select C.person_id, C.condition_era_id as event_id, C.condition_era_start_date as start_date,
       C.condition_era_end_date as end_date, CAST(NULL as bigint) as visit_occurrence_id,
       C.condition_era_start_date as sort_date
from 
(
  select ce.* 
  FROM CONDITION_ERA ce

) C


-- End Condition Era Criteria

) A on A.person_id = P.person_id  AND A.START_DATE >= P.OP_START_DATE AND A.START_DATE <= P.OP_END_DATE AND A.START_DATE >= (P.START_DATE + -365*INTERVAL'1 day') AND A.START_DATE <= (P.START_DATE + -1*INTERVAL'1 day') ) cc 
GROUP BY cc.person_id, cc.event_id
HAVING COUNT(cc.event_id) >= 1
-- End Correlated Criteria

  ) CQ on E.person_id = CQ.person_id and E.event_id = CQ.event_id
  GROUP BY E.person_id, E.event_id
  HAVING COUNT(index_id) = 1
) G
-- End Criteria Group
) AC on AC.person_id = pe.person_id AND AC.event_id = pe.event_id
) Results
;
ANALYZE Inclusion_0
;

CREATE TEMP TABLE inclusion_events

AS
SELECT
inclusion_rule_id, person_id, event_id

FROM
(select inclusion_rule_id, person_id, event_id from Inclusion_0) I;
ANALYZE inclusion_events
;
TRUNCATE TABLE Inclusion_0;
DROP TABLE Inclusion_0;


CREATE TEMP TABLE included_events

AS
WITH cteIncludedEvents(event_id, person_id, start_date, end_date, op_start_date, op_end_date, ordinal)  AS (
  SELECT event_id, person_id, start_date, end_date, op_start_date, op_end_date, row_number() over (partition by person_id order by start_date ASC) as ordinal
  from
  (
    select Q.event_id, Q.person_id, Q.start_date, Q.end_date, Q.op_start_date, Q.op_end_date, SUM(coalesce(POWER(cast(2 as bigint), I.inclusion_rule_id), 0)) as inclusion_rule_mask
    from qualified_events Q
    LEFT JOIN inclusion_events I on I.person_id = Q.person_id and I.event_id = Q.event_id
    GROUP BY Q.event_id, Q.person_id, Q.start_date, Q.end_date, Q.op_start_date, Q.op_end_date
  ) MG -- matching groups

  -- the matching group with all bits set ( POWER(2,# of inclusion rules) - 1 = inclusion_rule_mask
  WHERE (MG.inclusion_rule_mask = POWER(cast(2 as bigint),1)-1)

)
 SELECT
event_id, person_id, start_date, end_date, op_start_date, op_end_date

FROM
cteIncludedEvents Results
WHERE Results.ordinal = 1
;
ANALYZE included_events
;

-- date offset strategy

CREATE TEMP TABLE strategy_ends

AS
SELECT
event_id, person_id, 
  case when (start_date + 1*INTERVAL'1 day') > op_end_date then op_end_date else (start_date + 1*INTERVAL'1 day') end as end_date

FROM
included_events;
ANALYZE strategy_ends
;


-- generate cohort periods into #final_cohort
CREATE TEMP TABLE cohort_rows

AS
WITH cohort_ends (event_id, person_id, end_date)  AS (
	-- cohort exit dates
  -- End Date Strategy
SELECT event_id, person_id, end_date from strategy_ends

),
first_ends (person_id, start_date, end_date) as
(
	select F.person_id, F.start_date, F.end_date
	FROM (
	  select I.event_id, I.person_id, I.start_date, E.end_date, row_number() over (partition by I.person_id, I.event_id order by E.end_date) as ordinal 
	  from included_events I
	  join cohort_ends E on I.event_id = E.event_id and I.person_id = E.person_id and E.end_date >= I.start_date
	) F
	WHERE F.ordinal = 1
)
 SELECT
person_id, start_date, end_date

FROM
first_ends;
ANALYZE cohort_rows
;

CREATE TEMP TABLE final_cohort

AS
WITH cteEndDates (person_id, end_date)  AS (	
	SELECT
		person_id
		, (event_date + -1 * 0*INTERVAL'1 day')  as end_date
	FROM
	(
		SELECT
			person_id
			, event_date
			, event_type
			, MAX(start_ordinal) OVER (PARTITION BY person_id ORDER BY event_date, event_type ROWS UNBOUNDED PRECEDING) AS start_ordinal 
			, ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY event_date, event_type) AS overall_ord
		FROM
		(
			SELECT
				person_id
				, start_date AS event_date
				, -1 AS event_type
				, ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY start_date) AS start_ordinal
			FROM cohort_rows
		
			UNION ALL
		

			SELECT
				person_id
				, (end_date + 0*INTERVAL'1 day') as end_date
				, 1 AS event_type
				, NULL
			FROM cohort_rows
		) RAWDATA
	) e
	WHERE (2 * e.start_ordinal) - e.overall_ord = 0
),
cteEnds (person_id, start_date, end_date) AS
(
	SELECT
		 c.person_id
		, c.start_date
		, MIN(e.end_date) AS end_date
	FROM cohort_rows c
	JOIN cteEndDates e ON c.person_id = e.person_id AND e.end_date >= c.start_date
	GROUP BY c.person_id, c.start_date
)
 SELECT
person_id, min(start_date) as start_date, end_date

FROM
cteEnds
group by person_id, end_date
;
ANALYZE final_cohort
;

-- DELETE FROM @target_database_schema.@target_cohort_table where cohort_definition_id = @target_cohort_id;
-- INSERT INTO @target_database_schema.@target_cohort_table (cohort_definition_id, subject_id, cohort_start_date, cohort_end_date)
-- select @target_cohort_id as cohort_definition_id, person_id, start_date, end_date 
-- FROM final_cohort CO
-- ;




TRUNCATE TABLE strategy_ends;
DROP TABLE strategy_ends;


TRUNCATE TABLE cohort_rows;
DROP TABLE cohort_rows;

TRUNCATE TABLE final_cohort;
DROP TABLE final_cohort;

TRUNCATE TABLE inclusion_events;
DROP TABLE inclusion_events;

TRUNCATE TABLE qualified_events;
DROP TABLE qualified_events;

TRUNCATE TABLE included_events;
DROP TABLE included_events;

TRUNCATE TABLE Codesets;
DROP TABLE Codesets;