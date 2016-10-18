from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
	def namev(self, post):
		post = post.replace(' ', '')
		return (len(post) > 2) and post.isalpha()
	def email(self, post):
		return re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', post)
	def password(self, post):
		return len(post) >= 8
	def confirm(self, post, post1):
		return post == post1

class User(models.Model):
	name = models.CharField(max_length=200)
	alias = models.CharField(max_length=200)
	email = models.EmailField()
	password = models.CharField(max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	userManager = UserManager()

class Poke(models.Model):
	poker = models.ForeignKey(User, related_name='poker')
	pokee = models.ForeignKey(User, related_name='pokee')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)