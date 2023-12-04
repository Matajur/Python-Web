select p.fullname as professor, s.fullname as student, d.name as disc
from grades g 
join students s on s.id = g.student_id
join disciplines d on d.id = g.discipline_id
join professors p on p.id = d.professor_id 
where p.id = 1 and s.id = 1
group by p.fullname, s.fullname, d.name;
