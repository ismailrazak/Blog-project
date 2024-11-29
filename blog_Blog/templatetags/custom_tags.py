import markdown
from django import template

from ..models import Post

register = template.Library()
from django.db.models import Count
from django.utils.safestring import mark_safe


@register.simple_tag
def total_posts():

    lst = Post.objects.filter(status="PS")
    lst = lst.count()

    return lst


@register.inclusion_tag("latest_posts.html")
def latest_posts(count=4):
    latest = Post.objects.filter(status="PS").order_by("-publish")[:count]

    return {"latest": latest}


@register.simple_tag
def most_commented_posts():
    most_commented = (
        Post.objects.annotate(most_comments=Count("comments"))
        .order_by("-most_comments")
        .filter(status="PS")[:3]
    )
    most_commented = list(most_commented)

    return most_commented


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
