# Homework: Module 10 - Basics of working with Django

In the past homework, scraping of the site http://quotes.toscrape.com was made.

## Task

It is necessary to independently implement an analogue of such a site on Django.

1. Implement the possibility of registering on the site and entering the site.
2. The possibility of adding a new author to the site only for registered users.
3. The possibility of adding a new quote to the site with the author's name only for registered users.
4. Migrate your existing MongoDB database to Postgres for your site. Can be implemented with a custom script. (If you wish, you can leave and work with citations and authors in MongoDB, and with users in Postgres).
5. You can go to each author's page without user authentication.
6. All quotes are viewable without user authentication.

## Additional Task

7. Search for quotes by tags. When you click on a tag, a list of quotes with this tag is displayed.
8. Implement the "Top Ten tags" block and display the most popular tags.
9. Implement pagination. These are the next and previous buttons
10. Instead of transferring data from the MongoDB database, implement the possibility of scraping data directly from your site by pressing a certain button on the form and filling the site database;
11. Implement a password reset mechanism for a registered user;
12. All environment variables must be stored in the .env file and used in the settings.py file.
