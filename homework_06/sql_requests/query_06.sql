select g.name as group, s.fullname as student
from students s 
join groups g on g.id = s.group_id
where g.id = 1
order by s.fullname;
