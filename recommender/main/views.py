from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from main.models import ShelfEntry
from main.models import FavoriteGenres
import markdown2
from markdown2 import Markdown
import csv
import random
from pathlib import Path
from main.helpers import getresults
import matplotlib.pyplot as plt
from operator import itemgetter

import time
import numpy as np
import pandas as pd
import random
import operator
from operator import itemgetter
from statistics import mean 

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from django_postgres_extensions.models.functions import *

base_path = Path(__file__).parent
filepath = (base_path / "./df_books.csv").resolve()
df_books = pd.read_csv(filepath)

base_path_two = Path(__file__).parent
filepath_two = (base_path_two / "./df_tags.csv")
df_tags = pd.read_csv(filepath_two)

base_path_three = Path(__file__).parent
filepath_three = (base_path_two / "./df_ratings.csv")
df_ratings = pd.read_csv(filepath_three)

# df_books = pd.read_csv('/Users/may/Documents/GitHub/imdb-movie-recommender/recommender/main/df_books.csv' )
# df_tags = pd.read_csv('/Users/may/Documents/GitHub/imdb-movie-recommender/recommender/main/df_tags.csv' )


# Create your views here.

def home(request):
    return render(request, "home.html", {})

def login_view(request):
    return render(request, "login.html", {})

def signin(request): 
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/shelf')
    else: 
        return redirect('/login?error=True')

def signup(request):
    user = User.objects.create_user(
        username = request.POST['username'],
        password = request.POST['password'],
        email = request.POST['email']
    )
    login(request, user)
    return redirect('/shelf')



def shelf(request): 

    if not request.user.is_authenticated:
        return redirect('/login_view')


    entries = ShelfEntry.objects.filter(author=request.user)
    # matchedbooks = []
    # if request.method == "POST":
    #     title = request.POST["title"]
    #     reader = csv.reader(open('df_books.csv'))
    #     for row in reader:
    #         if title in row[title]:
    #             matchedbooks.append(row[title])
    return render(request, 'shelf.html', {'entries': entries})


def search(request):
    if request.method == "GET":
        searched = request.GET["title"]
        searched = str(searched)
        print("hello")
        print(type(searched))
        matchedbooks = getresults(searched)
    return render(request, 'results.html',{'searched': searched, 'matchedbooks': matchedbooks})

def results(request):
    pass
    # if request.method == "POST":
    #     entry = ShelfEntry(
    #         title = title,
    #         body = request.POST["body"],
    #         rating = request.POST["rating"]
    #     )
    #     entry.save()
    
    # return render(request,'results.html', {'title': title},{'entries': entries})

def addtoshelf(request, title):

    
    if request.method == "POST":
        entry = ShelfEntry.objects.create(
            title = title,
            review = request.POST["review"],
            rating = request.POST["rating"],
            author = request.user,
            genre = request.POST["genre"]
        )
        #entry.save()
        return redirect('/shelf')
    #print(entry.title)
    return render(request,'addtoshelf.html', {'title': title})

def get_book_titles(booklist):

    # Input: booklist: a list with book_ids
    # Output: titles_dict: dictionary with key: book_id, value: book title and author

    
    df_mask=df_books[df_books['book_id'].isin(booklist)]\
        [['book_id','title','authors']]
    titles_dict = dict(zip(df_mask['book_id'],\
        df_mask['title'].str.cat(df_mask[['authors']], sep=' - by: ')))
    
    return titles_dict


def genrerec(request):
    final_recommendations = dict()
    genreList = list()
    if request.method == "POST":  
        print("LSDFJFLKSDJFLKDSFJDS")
        genreObj = FavoriteGenres(
            genres = request.POST["choice"],
            author = request.user
        )
        genreObj.save()
        #books corresponding to user tag preferences.
        favesList = FavoriteGenres.objects.filter(author=request.user)
        for fave in favesList:
            genreList.append(fave.genres)
        print("tryinggggg")
        # print(genreList)
        df_book_filter=df_tags[df_tags['tag_id'].isin(genreList)]
        print("help")
        # print(df_book_filter)
        
        final_recommendations=get_book_titles(list(df_book_filter['book_id']))
        print(final_recommendations)
        final_recommendations = final_recommendations.values()
    return  render(request,'genrerec.html', {'recs': final_recommendations, 'genres': genreList})


def shelfrec(request):
    if not request.user.is_authenticated:
        return redirect('/login_view')

    final_recs = dict()
    books = list()
    recommendations = list()
    entries = ShelfEntry.objects.filter(author=request.user)

    ratings = dict()
    genres = list()
    for entry in entries:
        ratings[entry.title] = entry.rating
        genres.append(entry.genre)

    if request.method == "POST":  
        books.append(request.POST["choice"])

        #get a list of recommended books
        mean=weighted_mean(df_ratings, ratings, sample_size = 100)
        recommendations = list(map(itemgetter(0), mean))

        #get books within the genres of the books on the shelf
        df_book_filter=df_tags[df_tags['tag_id'].isin(genres)]
        #get books that are recommended based on the weighted mean
        df_book_filter=df_book_filter[df_book_filter['book_id'].isin(recommendations)]


        final_recs = getTitles(list(df_book_filter['book_id']))
        # print("LSKDFJ")
        # print("LSKDFJ")
        # print("LSKDFJ")
        # print("LSKDFJ")
        # print("LSKDFJ")
        # print(final_recs)

    return  render(request,'shelfrec.html', {'entries': entries, 'books': books, 'recs': final_recs})

def getTitles(IDlist):
    df_mask=df_books[df_books['book_id'].isin(IDlist)]\
        [['book_id','title','authors']]
    titlesList = dict(zip(df_mask['book_id'],\
        df_mask['title'].str.cat(df_mask[['authors']], sep=' - by: ')))
    
    return titlesList

def weighted_mean(df_ratings, ratings, sample_size = 100):

    random.seed(6)
    random_ids=random.sample(list(df_ratings['user_id'].unique()),sample_size) 
    
    df_reader_ratings=df_ratings[df_ratings['user_id'].isin(random_ids)].\
        groupby(['user_id', 'book_id'])['rating'].max().unstack()
           

    df_reader_ratings.loc[0] = None

  
    df_reader_ratings=df_reader_ratings.sort_index()


    for key in list(ratings.keys()):        
        df_reader_ratings.loc[0][key]=ratings.get(key)
        
    df_reader_ratings_dummy=df_reader_ratings.copy().fillna(0)
    
    cosine_ratings=cosine_similarity(df_reader_ratings_dummy,\
        df_reader_ratings_dummy)
    
    cosine_ratings=pd.DataFrame(cosine_ratings,index=df_reader_ratings.index,\
        columns=df_reader_ratings.index)

    book_wmeans={}
        
    cosine_reader=cosine_ratings[0]
            
    for book in list(df_reader_ratings.columns):
        
    #If book has not already been rated by the user:
        if book not in list(ratings.keys()):

            #ratings of the book in iteration by all readers.
            #all of the reader ratings for given book 'book'
            reader_ratings=df_reader_ratings[book] 

            #index containing the readers with NaN ratings.       
            #https://stackoverflow.com/questions/14016247/
            # find-integer-index-of-rows-with-nan-in-pandas-dataframe
            idx_nans = reader_ratings[reader_ratings.isnull()].index
    
            #ratings of the book in iteration by all readers without any NaNs.
            reader_ratings=df_reader_ratings[book].dropna()

            #remove the readers identified with NaN values.
            cosine_book=cosine_reader.drop(index=idx_nans)
        
            #carry out the dot product between both series. 
            # These do not contain NaN values.
            wmean_rating=np.dot(cosine_book,reader_ratings)/cosine_reader.sum()


            book_wmeans.update({book:wmean_rating})
    
    book_wmeans=sorted(book_wmeans.items(), key=operator.itemgetter(1),\
        reverse=True)
    
    return book_wmeans

def entry(request, id):
    entry = ShelfEntry.objects.get(id=id)
    return render(request, "entry.html", {'entry': entry}) 