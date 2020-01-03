from django.urls import path
from . import views 

urlpatterns=[
	path('', views.home, name = 'home'),
	path('movie-detail/', views.movie_detail, name = "detail"),
	path('add-to-favourite/', views.add_to_favourite, name = "add-to-favourite"),
	path('favourites-list/', views.FavouriteListView.as_view(), name = 'favourites')
]