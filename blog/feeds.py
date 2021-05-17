from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.utils.html import strip_tags


class RssBlogFeed(Feed):
    """
    Returns RSS Feed
    """
    title = 'ahampriyanshu'
    link = '/blog/'
    description = 'Latest articles of my blog'

    def items(self):
        """
        Returns a list of items to publish in this feed.
        """
        return Post.published.all().order_by('-publish')[:30]

    def item_title(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        title 
        """
        return item.title

    def item_link(self, item):
        """
        Takes an item, as returned by items(), and returns the item's URL.
        """
        return item.get_absolute_url()

    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        return item.author

    def item_description(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        description as a normal Python string.
        """
        return truncatewords(strip_tags(item.body).replace("\r\n", ""), 1000)


class AtomBlogFeed(RssBlogFeed):
    """
    Returns Atom Feed
    """
    feed_type = Atom1Feed
    subtitle = RssBlogFeed.description
