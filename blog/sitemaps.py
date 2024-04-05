from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import News


class ArticleSitemap(Sitemap):
    """
    Карта-сайта для статей
    """

    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return News.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class StaticSitemap(Sitemap):
    """
    Карта-сайта для статичных страниц
    """

    def items(self):
        return ['system:feedback', 'blog:news_request']

    def location(self, item):
        return reverse(item)