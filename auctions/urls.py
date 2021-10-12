from django.urls import path

from . import views 

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('register', views.register, name='register'),
	path('listing/<int:category_id>', views.listing, name='listing'),
	path('listings/<int:listing_id>', views.a_listing, name='a_listing'),
	path('categories', views.categories, name='categories'),
	path('bidding/<int:listing_id>', views.bidding, name='bidding'), 
	path('close_bidding/<int:listing_id', views.close_bidding, name='close_bidding'),
	path('add_watchlist/<int:listing_id>', views.add_watchlist, name='add_watchlist'),
	path('remove_watchlist/<int:listing_id>', views.remove_watchlist, name='remove_watchlist'),
	path('watchlist/<int:user_id>', views.watchlist, name='watchlist'),
	path('create_listing', views.create_listing, name='create_listing'),

]