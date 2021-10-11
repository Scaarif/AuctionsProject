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
		return self.category_name

class Listing(models.Model):
	""" An active listing in a given category """
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	listing = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add = True)
	description = models.TextField()

	def __str__(self):
		"""Return a string representation of the model."""
		return f"{self.listing}: {self.description}" 


class Comment(models.Model):
	"""Comments by users on a particular listing"""
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	comment = models.TextField(max_length=200)
	date_added = models.DateTimeField(auto_now_add = True)


	def __str__(self):
		"""Return a string representation of the model."""
		return self.comment


class Bid(models.Model):
	"""Bids placed on a listing by users"""
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
	initial_bid = models.IntegerField()
	#current_bid = models.IntegerField()

	def __str__(self):
		"""Return a string representation of the model."""
		#return f"The listing bid was ksh.{self.initial_bid} and is currently at ksh.{self.current_bid}"
		return f"The listing is at ksh.{self.initial_bid}"

