from django.urls import path

from . import views 

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('register', views.register, name='register'),
	path('listing/<int:category_id>', views.listing, name='listing'),
	path('a_listing/<str:listing_title>', views.a_listing, name='a_listing'),
	path('categories', views.categories, name='categories'),

]