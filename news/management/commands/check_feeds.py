from django.core.management.base import BaseCommand, CommandError


from news.models import Article, Feed
import newspaper
import datetime
import feedparser

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
 
        # form = FeedForm(request.POST)
        # if form.is_valid():
        #     feed = form.save(commit=False)

        #     exitingFeed = Feed.objects.filter(url = feed.url)
        #     if len(exitingFeed) ==0:

####################################

            feeds = Feed.objects.all()
            # for feed in feeds:    

                # feedData = feedparser.parse(feed.url)
                # # set same fields
                # feed.title = feedData.feed.title
                # feed.save()


                # for entry in feed.entries:
                # for feed_url in Feed.objects.all().values_list("url", flat=True):

            for feed in feeds:
                feedData = feedparser.parse(feed.url)
                # set same fields

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
                    #article.title = a.title


                    d = datetime.datetime(*(entry.published_parsed[0:6]) )
                    dateString = d.strftime('%Y-%m-%d %H:%M:%S')

                    article.publication_date = dateString
                    article.feed = feed
                    article.save()




        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))