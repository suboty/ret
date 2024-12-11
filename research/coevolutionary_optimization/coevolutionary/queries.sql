-- get avg minimum for experiment by metric
with avg_minimums as (
	select
	    s.algorithm_name as name,
	    s.iteration as iteration,
	    avg(s.minimum) as avg_minimum
	from statistics s
	where s.experiment_name = 1
	group by
	    s.algorithm_name, s.iteration
)
select * from avg_minimums
where name like '%metric_1'
;

-- get avg iteration quality for experiment by metric
with avg_qualities as (
	select
	    q.algorithm_name as name,
	    q.iteration as iteration,
	    avg(quality) as avg_quality
	from qualities q
	where q.experiment_name = 1
	group by
	    q.algorithm_name, q.iteration
)
select * from avg_qualities
where name like '%metric_1'
;

-- get avg invalid individuals number for experiment by metric
with avg_invalid_ind as (
	select
	    s.algorithm_name as name,
	    s.iteration as iteration,
	    avg(s.invalid_ind) as avg_invalid_ind
	from statistics s
	where s.experiment_name = 1
	group by
	    s.algorithm_name, s.iteration
)
select * from avg_invalid_ind
where name like '%metric_1'
;

-- get popular regex for experiment by metric
with popular_regex as (
	select
		output_regex as regex,
		count(*) as regex_count
	from experiments e
	where
		experiment_name = 1
		and algorithm_name like '%metric_1'
	group by output_regex
)
select * from popular_regex
order by regex_count desc
;