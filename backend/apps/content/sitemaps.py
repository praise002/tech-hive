from apps.content.models import Article
from django.contrib.sitemaps import Sitemap


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Article.objects.published().all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/api/v1/articles/{obj.slug}"
