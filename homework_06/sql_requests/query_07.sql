select g2.name as "group", d.name as disc, s.fullname as student, g.grade, g.date_of 
from grades g 
join students s on s.id = g.student_id
join disciplines d on d.id = g.discipline_id
join "groups" g2 on g2.id = s.group_id 
where d.id = 1 and g2.id = 1
group by g2.name, d.name, s.fullname, g.grade, g.date_of
