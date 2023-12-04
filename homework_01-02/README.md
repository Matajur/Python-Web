# Combined Homework of Modules 1-2


# Homework: Module 1 - Techniques of object-oriented programming

## Task

1.  Draw a UML diagram of the 'Personal Assistant' graduation project from previous course.
    For work, you can use the free draw.io or any other application convenient for you.

2.  Your previous application is now running in console mode and interacting with the user as commands in the console.
    The application needs to be developed and the part of the application that changes the most is usually the user interface (so far it's the console).
    Modify the code of your application so that the presentation of information to the user (displaying cards with the user's contacts, notes, a page with information about the available commands) is easy to change.
    This requires describing an abstract base class for custom views and concrete implementations that emulate the base class and implement the console interface.

https://app.slack.com/client/T05B7EFE14J/C05CEHH55U5

## Diagram

![UML-Diagram](https://github.com/Matajur/Python-Web/homework_01/blob/main/UML-Diagram.pdf)


# Homework: Module 2 - Python Development

## Task

1. Right now, the 'Personal Assistant' project most likely exists as a package on the system, installed globally, and uses the version of Python that is installed on the system with the packages installed on the system.
   Use any convenient pipenv or poetry tool of choice to create a virtual environment for the application.
   Fix the version of Python in this environment (specify clearly: which Python should be used) and configure the IDE to work with the created environment.
   If third-party projects were used, they should also now have a specific version.

2. Create a Dockerfile in which you install Personal Assistant and run it as a separate application in a separate container.