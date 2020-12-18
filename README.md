# GoodReads Book Recommender
We used the a book database from the site GoodReads to create a book recommender website. We built the site with Django, and to pull and parse our data in the format of a CSV file, we  used the following libraries: 

For code requirements, our first party-packages were csv, random, time, numpy, pandas, pathlib, operator, statistics, and matplotlib.pyplot. Our third party packages are Django, psycopg2-binary, django_postgres_extensions.models, and sklearn. 

We have two classes, ShelfEntry and FavoriteGenres. 

Structurally, we do the most work within views.py. We decided to put our recommendation algorithms within views.py as we had two different recommenders, genre and current shelf and we wanted to display those as links from the "my shelf" page. For everything else, we used models and the User model to ensure that a user had their own tailored experience.


## To Run

* Download all files
* Open terminal and enter "cd recommender"
* Make sure you have django installed - if not, enter in terminal "pip install django"
* Enter the following commnds:
  * python manage.py makemigrations
  * python manage.py migrate
  * python manage.py server
* Access the website on: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Make an account 
* Happy reading!


## Resources:
* [Link to Kaggle GoodReads](https://www.kaggle.com/jealousleopard/goodreadsbooks)
