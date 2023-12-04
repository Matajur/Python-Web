select p.fullname as professor, d.name as disc, round(avg(g.grade), 2) as av_grade
from grades g 
join disciplines d on d.id = g.discipline_id
join professors p on p.id = d.professor_id 
where p.id = 4
group by p.fullname, d.name;
