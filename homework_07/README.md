# Homework: Module 7 - ORM SQLAIchemy

## Introduction

In this homework assignment, we will continue with the homework assignment from the previous module.

In this homework, the postgres database will be used. At the command line, start the Docker container:

docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

Instead of some-postgres, choose the container name, and instead of mysecretpassword, come up with the database connection password.

## Homework Steps

### 1st Step
Implement the SQLAlchemy models for tables:

* Table of students;
* Table of groups;
* Table of professors;
* Table of subjects with an indication of the professor who reads the subject;
* A table where each student has grades in subjects with an indication of when the grade was received.

### 2nd Step
Use alembic to create database migrations.

### 3rd Step
Write a seed.py script and fill the resulting database with random data (~30-50 students, 3 groups, 5-8 subjects, 3-5 professors, up to 20 grades for each student in all subjects). Use the Faker pack to fill. When filling, we use the SQLAlchemy session mechanism.

### 4th Step
Make the following selections from the obtained database:

01. Find the 5 students with the highest GPA in all subjects.
02. Find the student with the highest GPA in a particular subject.
03. Find the average score in groups for a certain subject.
04. Find the average score on the stream (across the entire scoreboard).
05. Find out what courses a particular professor teaches.
06. Find a list of students in a certain group.
07. Find the grades of students in a separate group for a certain subject.
08. Find the average score given by a certain professor in his subjects.
09. Find a list of courses attended by a particular student.
10. A list of courses taught to a particular student by a particular professor.

For requests, create a separate file my_select.py, where there will be 10 functions from select_1 to select_10. Execution of functions should return a result similar to the previous homework. For requests, we use the SQLAlchemy session mechanism.

## Hints

This task will test ability to use the SQLAlchemy documentation. Let's have the following query.

Find the 5 students with the highest GPA across all subjects.
Let's try to turn it into an ORM SQLAlchemy query. Let us have a session in the session variable. The Student and Grade models for the corresponding tables are described. We believe that the database is already filled with data. SQLAlchemy stores aggregation functions in the func object. It needs to be specially imported from sqlalchemy import func and then we can use the func.round and func.avg methods. So the first line of the SQL query should look like this session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')). Here we also used label('avg_grade') so the ORM performs field naming, with the average grade, using the AS operator.

Next, FROM grades g is replaced by the select_from(Grade) method. Replacing the JOIN operator - everything here is simply the join(Student) function, everything else is taken care of by the ORM. We perform grouping by field using the group_by(Student.id) function.

The order_by function is responsible for sorting, which, by default, sorts as ASC, and we clearly need the DESC ascending mode and also by the avg_grade field, which we ourselves created in the query. We import from sqlalchemy import func, desc and the final form is order_by(desc('avg_grade')). A limit of five values is a function with the same name limit(5). That's all, our request is ready.

The final query option for the SQLAlchemy ORM.
Construct other requests similarly to the example above. One last tip, in case of decision to make nested queries then use scalar-selects.

## Additional Task

### 1st Part
For an additional task, make the following requests of increased complexity:

11. The average score given by a certain teacher to a certain student.
12. Grades of students in a certain group on a certain subject in the last lesson.

### 2nd Part
Instead of a seed.py script, consider and implement a full CLI application for CRUD database operations. Use the argparse module for this.

Use the --action command or the shortened option -a for CRUD operations. And the --model (-m) command to specify which model to operate on.

### Example

* --action create -m Professor --name 'Boris Jonson' (to create professor)
* --action list -m Professor (show all professors)
* --action update -m Professor --id 3 --name 'Andry Bezos' (update professor's data with id=3)
* --action remove -m Professor --id 3 (remove professor with id=3)

Perform these operations for each model.

### INFO
Examples of executing commands in the terminal.

Create professor

 py main.py -a create -m Professor -n 'Boris Jonson'

Greate group

 py main.py -a create -m Group -n 'AD-101'  
