select p.fullname as professor, d.name as disc
from disciplines d
join professors p on p.id = d.professor_id
where p.id = 1
order by d.name;
