from apps.content.models import Article
from decouple import config
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html


class LatestArticlesFeed(Feed):
    title = "Tech Hive"

    if settings.DEBUG:
        link = config("FRONTEND_URL_DEV")
    else:
        link = config("FRONTEND_URL_PROD")

    # link = "/api/v1/articles/"
    description = "New posts of Tech Hive."

    def items(self):
        return Article.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(item.content, 30)

    def item_pubdate(self, item):
        return item.published_at

    def item_link(self, item):
        # This provides individual article links
        # return f"/articles/{item.slug}/"
        return f"{self.link}/articles/{item.slug}/"
