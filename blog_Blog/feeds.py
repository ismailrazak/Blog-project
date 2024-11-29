import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from .models import Post


class Feeds(Feed):
    title = "My blog"
    link = reverse_lazy("blog_Blog:post_list")
    description = "Blog posts about day to day things."

    def items(self):
        return Post.objects.filter(status="PS").order_by("-publish")[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 5)

    def item_pubdate(self, item):
        return item.publish
