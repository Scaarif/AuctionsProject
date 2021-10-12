from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import User, Category, Listing, Bid, Comment

# Create your views here.

def index(request):
	listings = Listing.objects.filter(sold=False)
	return render(request, 'auctions/index.html', {'listings':listings})

def categories(request):
	categories = Category.objects.all()
	context = {'categories':categories}
	return render(request, 'auctions/categories.html', context )

def a_listing(request, listing_title):
	listing = Listing.objects.filter(title=listing_title)

	return render(request, 'auctions/a_listings.html', {'listing':listing})

def login_view(request):
	if request.method == "POST":

		#Attempt to sign the user in
		username=request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		#Check if authentication was successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "auctions/login.html",{
				"message":"Invalid username and/or password."
				})
	else:
		return render(request, "auctions/login.html")
def logout_view(request):
 	logout(request)
 	return HttpResponseRedirect(reverse("index"))

def register(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']

		#Ensure password nmatches confirmation
		password = request.POST['password']
		confirmation = request.POST['confirmation']
		if password != confirmation:
			return render(request, "auctions/register.html", {"message":"Passwords must match"})
		#Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, 'auctions/register.html', {'message':'Username already taken.'})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, 'auctions/register.html')


def listing(request, category_id):
	'''Return listings under a category'''
	category = Category.objects.get(id=category_id)
	listings = category.listing_set.all()
	return render(request, 'auctions/listing.html', {"category":category, "listings":listings})

##
@login_required
def listing_info(request, listing_id):
	listing = Listing.objects.get(id=listing_id)
	user = request.user
	is_owner = True if listing.user == user else False
	category = Category.objects.get(category=listing.category)
	comments = Comment.objects.filter(listing=listing.id)
	watching = Watchlist.objects.filter(user=user, listing=listing)
	if watching:
		watching = Watchlist.objects.get(user=user, listing=listing)

	return listing, user, is_owner, category, comments, watching 

	







