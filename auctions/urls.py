from django.urls import path

from . import views 

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),
	path('register', views.register, name='register'),
	path('listings/<int:category_id>', views.listings, name='listings'),
	#path('all_listings', views.all_listings, name='all_listings'),
	path('categories', views.categories, name='categories'),

]