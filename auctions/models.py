from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
	pass 
class Category(models.Model):
	"""Grouping of auction listings on particular basis say fashion or furniture"""
	category_name = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = 'categories'
	
	def __str__(self):
		"""Return a string representation of the model."""
		return f"{self.category_name}"

class Listing(models.Model):
	""" An active listing in a given category """
	user = models.ForeignKey(User, on_delete=models.CASCADE) #the user who posted the listing
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add = True)
	description = models.TextField()
	listing_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
	sold = models.BooleanField(default=False)
	image_url = models.URLField(default='google.com')
	categories = models.ManyToManyField(Category, blank=True, related_name="select_category") #all categories to select from


	def __str__(self):
		"""Return a string representation of the model."""
		return f"{self.description}" 


class Comment(models.Model):
	"""Comments by users on a particular listing"""
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	comment = models.TextField(max_length=200)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add = True)


	def __str__(self):
		"""Return a string representation of the model."""
		return f"{self.comment} - {self.user}"


class Bid(models.Model):
	"""Bids placed on a listing by users"""
	user = models.ForeignKey(User, on_delete=models.CASCADE,)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	bid_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
	#current_bid = models.IntegerField()

	def __str__(self):
		"""Return a string representation of the model."""
		#return f"The listing bid was ksh.{self.initial_bid} and is currently at ksh.{self.current_bid}"
		return f"Bid on item: {self.listing}  by {self.user} at ksh.{self.bid_price}"

class Watchlist(models.Model):
	"""Keeps track of whether a listing is in a users watchlist"""
	user = models.ForeignKey(User, on_delete=models.CASCADE,)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	watching = models.BooleanField(default=False)




