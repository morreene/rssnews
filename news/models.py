from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Feed(models.Model):
	title = models.CharField(max_length=200)
	url = models.URLField()
	is_active = models.BooleanField(default=False)

	def __str__(self):
		return self.title.encode('utf8')


class Article(models.Model):
	feed = models.ForeignKey(Feed)
	title = models.CharField(max_length=200)
	url = models.URLField()
	description = models.TextField()
	keyword = models.TextField()
	full = models.TextField()
	publication_date = models.DateTimeField()

	#def __str__(self):
	def __str__(self):
		return self.title.encode('utf8')


