from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views.generic import ListView
import requests
from django.contrib import messages
from .models import Favourite

url = 'https://www.omdbapi.com/?s={}&apikey=82793b2a'
search_list = [] #creating an empty list so that it can be appended with API fetched data

def home(request):
	if request.method == 'GET':
		title = request.GET.get('title')
		r = requests.get(url.format(title)).json() # Getting data from API in json format

		# Checking if the data input by the user is valid or not
		if r['Response'] == 'False':
			messages.error(request, f'No movie named "{title}" found!')	
			return redirect('home')

		# sending the fetched data to frontend, search_list is cleared with every new call.
		else:
			search_list.clear()
			for movie in r['Search']:		
				search_list.append(movie['Title'])
			context = {
				'search_list': search_list,
				'title': title
			}
			return render(request, 'movie_search/home.html', context)

	# Displaying the homepage without any data when first opened
	else:		
		return render(request, 'movie_search/home.html') #sending the user to home page when no form is submitted

def movie_detail(request):
	if request.method == "GET":
		title = request.GET.get('search_list_element') # fetching the movie title clicked by the user
		r = requests.get(url.format(title)).json()

		# Checking if the data is valid or not
		if r['Response'] == 'False':
			messages.error(request, f'Sorry but the details of this movie are currently unavailable')	
			return redirect('home')

		# sending the fetched data to the frontend to display details. Flags are used to check if the selected the movie is in favourites.
		else:
			object_list = Favourite.objects.all()
			title_list = []
			for item in object_list:
				title_list.append(item.title)
			flag = True
			print(r['Search'][0]['Title'])
			print(object_list)
			if r['Search'][0]['Title'] in title_list:
				flag = False
			context = {
				'title': r['Search'][0]['Title'],
				'year': r['Search'][0]['Year'],
				'type': r['Search'][0]['Type'],
				'poster': r['Search'][0]['Poster'],
				'flag': flag	
			}
				
			return render(request, 'movie_search/detail.html', context)
	else:
		return HttpResponseForbidden() # if someone tries to access the link directly; they get a forbidden message and the app does not break.

def add_to_favourite(request):

	# Creating a record in the database for the movie selected to be a favourite
	if request.method == "POST":
		Favourite.objects.create(title = request.POST.get('title'))
		messages.success(request, f'Movie successfullly added to favourites!')
		return redirect('home')

# Taking advantage of the aleady available "class-based views" in django to minimize the lines of code.
class FavouriteListView(ListView):
	model = Favourite
	