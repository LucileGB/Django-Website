# P9_Lucile_GARRIGOUX
This is a web app using Django and SQlite. Its aim is to allow users to create, edit or delete requests for reviews about books and articles.

People can follow other users to see their requests or answer their tickets with reviews.

## SETTING UP YOUR ENVIRONMENT AND LAUNCHING THE PROJECT
To launch the project, first download the relevant files. Once you've installed the virtual environment of your choice, please install the content of requirement.txt:

> pip install -r requirements.txt

Then, navigate with the console up to the folder where you've installed the application. Ensure that you are at the same folder level than manage.py. **If you wish to start a new database, delete the file db.sqlite3 and type the following:**

> python manage.py makemigrations

> python manage.py migrate

To be able to interact with the app, you will need to create a superuser. To do so, type the following once migration is done:

> python manage.py createsuperuser

You can now interact with the app as described below.

**If you wish to keep the test database, please proceed below**.

## INTERACTING WITH THE APP
To be able to interact with the app, you need to launch the server. To do so, navigate with the conole up to the folder where you've installed the application and type the following:

> python manage.py runserver

This will launch the server, ensuring that the site is working locally. If you kept the test database, admin ids are the followings:

Username:  LucileG

Password: HYPATIAè

You can now interact with Django's admin console at http://127.0.0.1:8000/admin/, or you can explore the project at http://127.0.0.1:8000/. You can create users either in the admin console or through the login screen.
