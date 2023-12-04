select s.fullname as student, d.name as disc
from grades g 
join students s on s.id = g.student_id
join disciplines d on d.id = g.discipline_id
where s.id = 1
group by s.fullname, d.name
order by d.name;
