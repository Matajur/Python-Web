# Homework: Module 6 - Relational databases

## Task

Implement a database which schema contains:

* Table of students;
* Table of groups;
* Table of professors;
* A table of subjects with an indication of the professors who reads the subject;
* A table where each student has grades in subjects with an indication of when the grade was received.

Fill the resulting database with random data (~30-50 students, 3 groups, 5-8 subjects, 3-5 teachers, up to 20 grades for each student in all subjects). Use the Faker pack to fill.

Make the following selections from the obtained database:

1. Find the 5 students with the highest GPA across all subjects.
2. Find the student with the highest GPA in a particular subject.
3. Find the average score in groups for a certain subject.
4. Find the average score on the stream (across the entire scoreboard).
5. Find what courses a particular professor teaches.
6. Find a list of students in a certain group.
7. Find the grades of students in a separate group on a certain subject.
8. Find the average score given by a certain professor in his subjects.
9. Find the list of courses attended by the student.
10. A list of courses taught to a particular student by a particular professor.

For each request, issue a separate query_number.sql file, where instead of number, substitute the number of the request. The file contains an SQL statement that can be executed either in the database terminal or via cursor.execute(sql).

## Additional Task

For an additional task, make the following requests of increased complexity:

11. The average score given by a particular professor to a particular student.
12. Grades of students in a certain group in a certain subject in the last lesson.
