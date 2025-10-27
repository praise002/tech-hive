from django.contrib.sitemaps import Sitemap

from apps.content.models import Article
 
class ArticleSitemap(Sitemap):
    changefreq ='weekly'
    priority = 0.9
    
    def items(self):
        return Article.published.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return f'/api/v1/articles/{obj.slug}'