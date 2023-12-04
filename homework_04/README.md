# Homework: Module 4 - Web Basics

# Task

The goal is to implement the simplest web application. Take the following files as a basis.

https://drive.google.com/file/d/1WYxNO5ymmkH0yMY0cJUgtzE0rcKC1njP/view

Create a web application with routing for two html pages: index.html and message.html.

Also:

* Process static resources during application operation: style.css, logo.png;
* Organize work with the form on the message.html page;
* If a 404 Not Found error occurs, return the error.html page;
* The application is running on port 3000.

To work with the form, create a Socket server on port 5000. The work algorithm is as follows. User enters data in the form, it enters the web application, which forwards it further for processing using a socket (UDP protocol) Socket server. The Socket server converts the received byte string into a dictionary and saves it in json file data.json in the storage folder.

The recording format of the data.json file is as follows:

{
  "2022-10-29 20:20:58.020261": {
    "username": "krabaton",
    "message": "First message"
  },
  "2022-10-29 20:21:11.812177": {
    "username": "Krabat",
    "message": "Second message"
  }
}

Where the key of each message is the time of receiving the message: datetime.now(). That is, each new message from the web application is added to the storage/data.json file with the time of receipt.

Use one main.py file to build the web application. Start the HTTP server and the Socket server in different threads.

## Additional Task

1. Create a Dockerfile and run the application as a Docker container;
2. Using the volumes mechanism, store data from storage/data.json outside of the container.
3. To implement the volumes mechanism, it's needed to check the existence of the storage directory and the data.json file at the start of the application. And if they are missing, then create them.
