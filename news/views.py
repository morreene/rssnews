from django.shortcuts import render
from .models import Article, Feed
from .forms import FeedForm
from django.shortcuts import redirect
import feedparser
import datetime
import newspaper
#from django.utils import timezone
# from readability.readability import Document
# import urllib


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def articles_list(request):
	articles_l = Article.objects.all().order_by("-publication_date")
	paginator = Paginator(articles_l, 10) # Show 25 contacts per page
	# rows = [articles[x:x+1] for x in range(0,len(articles), 1)]
	# return render(request, 'news/articles_list.html', {'rows':rows})

	page = request.GET.get('page')
	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		articles = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		articles = paginator.page(paginator.num_pages)
	return render(request, 'news/articles_list.html', {'articles':articles})


def feeds_list(request):
	feeds = Feed.objects.all()
	return render(request, 'news/feeds_list.html', {'feeds':feeds})

def full_article(url):
	html = urllib.urlopen(url).read()
	readable_article = Document(html).summary()
	# readable_title = Document(html).short_title()
	return readable_article

def new_feed(request):
	if request.method=="POST":
		form = FeedForm(request.POST)
		if form.is_valid():
			feed = form.save(commit=False)

			exitingFeed = Feed.objects.filter(url = feed.url)
			if len(exitingFeed) ==0:
				feedData = feedparser.parse(feed.url)
				# set same fields
				feed.title = feedData.feed.title
				feed.save()

				for entry in feedData.entries:
					article = Article()
					article.title = entry.title
					article.url = entry.link
					article.description = entry.description
					# article.full = full_article(entry.link)

					a = newspaper.Article(entry.link, language='en') 
					a.download()
					a.parse()
					a.nlp()
					article.keyword = a.keywords
					article.full = a.text


					d = datetime.datetime(*(entry.published_parsed[0:6]) )
					dateString = d.strftime('%Y-%m-%d %H:%M:%S')

					article.publication_date = dateString
					article.feed = feed
					article.save()

			return redirect('news.views.feeds_list')
	else:
		form = FeedForm()
	return render(request, 'news/new_feed.html', {'form': form})


