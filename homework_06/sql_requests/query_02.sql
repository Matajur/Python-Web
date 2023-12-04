select d.name as disc, s.fullname as student, round(avg(g.grade), 2) as av_grade
from grades g 
join students s on s.id = g.student_id
join disciplines d on d.id = g.discipline_id
where d.id = 1
group by s.fullname, d.name
order by av_grade desc
limit 1;
