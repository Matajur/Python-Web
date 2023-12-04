select s.fullname as student, round(avg(g.grade), 2) as av_grade
from grades g 
join students s on s.id = g.student_id 
group by s.fullname 
order by av_grade desc 
limit 5;
