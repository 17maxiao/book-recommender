# GoodReads Book Recommender
We used the a book database from the site GoodReads to create a book recommender website. We built the site with Django, and to pull and parse our data in the format of a CSV file, we  used the following libraries: 

* numpy
* pandas 
* statistics

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


## Pages

###### My Shelf
The homepage which contains all of the books that you have added to your shelf - use the search bar to look for the title of the book that you want to add. Then, the webpage will navigate you to the a page to select among a list of results for the title you want to add. Once you choose the title of your choice, enter the following information:

* your review
* book rating
* book genre (your personal categorization!)

Once you submit the book review, it will show up on your shelf!

###### Recommend by My Favorite Genres

Select genres to filter suggested books by! We use pandas to filter the dataframe by the selected genres.

###### Recommend by My Books on Shelf

We will pull recommendations based on a weighted mean function on ratings for books based on the ones on your shelves!


## Resources:
* [Link to Kaggle GoodReads](https://www.kaggle.com/jealousleopard/goodreadsbooks)
