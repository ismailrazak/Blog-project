from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from taggit.models import Tag

from .models import Post


class PostSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(status="PS")

    def lastmod(self, obj):
        return obj.updated


class TagSiteMap(Sitemap):
    change_freq = "weekly"
    priority = 0.8

    def items(self):
        return Tag.objects.all()

    def location(self, item):
        return reverse("blog_Blog:tags_list", args=[item.slug])
