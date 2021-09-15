# P9_Lucile_GARRIGOUX
This is a web app using Django and SQlite. Its aim is to allow users to create, edit or delete requests for reviews about books and articles.

People can follow other users to see their requests or answer their tickets with reviews.

## LAUNCHING THE PROJECT
To launch the project, first download the relevant files. Once you've installed the virtual environment of your choice, please install the content of requirement.txt.

Then, navigate with the console up to the folder where you've installed the application. Ensure that you are at the same folder level than manage.py and type the following:

> python manage.py magemigrations

> python manage.py migrate

Wait for the process to finish, then type

> python manage.py runserver

## INTERACTING WITH THE APP
To be able to interact with the app, you need to create a superuser. To do so, navigate with the conole up to the folder where you've installed the application and type the following:

> python manage.py createsuperuser

Fill in the relevant information. You can now interact with Django's admin console at http://127.0.0.1:8000/admin/, or you can explore the project at http://127.0.0.1:8000/reviews.
