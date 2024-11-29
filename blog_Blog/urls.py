from django.urls import path

from . import views
from .feeds import Feeds

app_name = "blog_Blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("tags/<slug:tag_slug>/", views.post_list, name="tags_list"),
    # path('',views.PostlistView.as_view(),name='post_list'),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/",
        views.single_post,
        name="single_post",
    ),
    path("<int:id>/share/", views.post_share, name="share_form"),
    path("<int:id>/comments/", views.comment_view, name="comment"),
    path("feeds/", Feeds(), name="feeds"),
    path("search/", views.searchform, name="search"),
]
