select d.name as disc, g2.name as "group", round(avg(g.grade), 2) as av_grade
from grades g 
join students s on s.id = g.student_id
join disciplines d on d.id = g.discipline_id
join "groups" g2 on g2.id = s.group_id 
where d.id = 1
group by g2.name, d.name
order by av_grade desc;
