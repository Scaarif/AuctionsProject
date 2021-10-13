from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import User, Category, Listing, Bid, Comment, Watchlist
from .forms import CreateListingForm

# Create your views here.

def index(request):
	listings = Listing.objects.filter(sold=False)
	return render(request, 'auctions/index.html', {'listings':listings})

def categories(request):
	categories = Category.objects.all()
	context = {'categories':categories}
	return render(request, 'auctions/categories.html', context )

'''def a_listing(request, listing_title):
	listing = Listing.objects.filter(title=listing_title)

	return render(request, 'auctions/a_listings.html', {'listing':listing})'''

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


def a_listing(request, listing_id):
	info = listing_info(request, listing_id)
	listing, user, is_owner, category = info[0], info[1], info[2], info[3]

	if request.method == 'POST':
		comment = request.POST['comment']
		if comment != '': 
			Comment.objects.create(user = user, listing = listing, comment = comment)
	return render(request, 'auctions/a_listing.html', {
		'listing':listing,
		'category': category,
		'comments': Comment.objects.filter(listing=listing.id),
		'watching':Watchlist.objects.filter(user = user, listing = listing).values('watching'),
		'is_owner': is_owner
		})

@login_required
def bidding(request, listing_id):
	info = listing_info(request, listing_id)
	listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
	if request.method == 'POST':
		bid = request.POST['bid']
		listing.listing_price = float(bid) #update the price as par bid
		listing.save()
		Bid.objects.create(user = user, bid_price = bid, listing = listing)

	return render(request, 'auctions/a_listing.html', {
		'listing': listing,
		'category': category,
		'comments': comments,
		'watching': watch,
		'is_owner': is_owner
		})

@login_required
def close_bidding(request, listing_id):
	info = listing_info(request, listing_id)
	listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
	listing.sold = True
	listing.save()
	winner = Bid.objects.get( bid_price = listing.listing_price, listing = listing).user 
	print(user.id, winner.id)
	is_winner = user.id == winner.id 

	return render(request, 'auctions/close_bidding.html', {
		"listing": listing,
        "category": category,
        "comments": comments, 
        "watching": watch, 
        "is_owner": is_owner,
        "is_winner": is_winner
		})

@login_required
def watchlist(request):
	listing_ids = Watchlist.objects.filter(user = request.user, watching=True).values('listing')
	listings = Listing.objects.filter(id__in = listing_ids)
	return render(request, 'auctions/watchlist.html', {
		'listings': listings
		})

@login_required
def add_watchlist(request, listing_id):
	info = listing_info(request, listing_id)
	listing, user, is_owner, category, comments = info[0], info[1], info[2], info[3], info[4]
	watch = Watchlist.objects.filter(user = user, listing = listing)
	if watch:
		watch = Watchlist.objects.get(user = user, listing = listing)
		watch.watchting = True
		watch.save()
	else:
		Watchlist.objects.create(user = user, listing = listing, watching = True)

	return render(request, 'auctions/a_listing.html', {
		'listing': listing,
		'category': category,
		'comments': comments,
		'watching': Watchlist.objects.get(user = user, listing = listing).watching,
		'is_owner': is_owner
		})

@login_required
def remove_watchlist(request, listing_id):
	info = listing_info(request, listing_id)
	listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
	watch.watching = False
	watch.save()
	return render(request, "auctions/a_listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments, 
        "watching": WatchList.objects.get(user = user, listing = listing).watching, 
        "is_owner": is_owner
    })
@login_required
def create_listing(request):
	if request.method =='POST':
		form = CreateListingForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			description = form.cleaned_data['description']
			bid = form.cleaned_data['bid']
			image_url = form.cleaned_data['image_url']
			user = request.user
			category_id = Category.objects.get(id=request.POST['categories'])
			Listing.objects.get_or_create(user = user, title = title, description = description,
			listing_price = bid, image_url = image_url, category = category_id)
		return HttpResponseRedirect(reverse('index'))

	else:
		return render(request, 'auctions/create_listing.html', {
			'listing_form':CreateListingForm(),
			'categories': Category.objects.all()
			})



			




	







