-- get avg minimum for experiment
select
    s.algorithm_name as name,
    s.iteration as iteration,
    avg(s.minimum) as avg_minimum
from statistics s
where s.experiment_name = NUMEXP
group by
    s.algorithm_name, s.iteration
;

-- get avg iteration quality for experiment
select
    q.algorithm_name as name,
    q.iteration as iteration,
    avg(quality) as avg_quality
from qualities q
where q.experiment_name = NUMEXP
group by
    q.algorithm_name, q.iteration
;

-- get avg invalid individuals number for experiment
select
    s.algorithm_name as name,
    s.iteration as iteration,
    avg(s.invalid_ind) as avg_invalid_ind
from statistics s
where s.experiment_name = NUMEXP
group by
    s.algorithm_name, s.iteration
;