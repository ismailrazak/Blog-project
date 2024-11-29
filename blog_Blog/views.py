from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, SearchForm, ShareForm
from .models import Comment, Post


def post_list(request, tag_slug=None):
    posts_list = Post.objects.filter(status="PS")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    paginator = Paginator(posts_list, 3)
    page_no = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_no)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, "post_list.html", {"posts": posts, "tag": tag})


def single_post(request, year, month, day, slug):
    post = Post.objects.get(
        publish__year=year, publish__month=month, publish__day=day, slug=slug
    )
    print(post.tags)
    # post=get_object_or_404(Post,publish__year=year,publish__month=month,publish__day=day,slug=slug)
    tag_ids = post.tags.values_list("id", flat=True)
    tag_ids = list(tag_ids)
    similar_posts = Post.objects.filter(status="PS", tags__in=tag_ids).exclude(
        id=post.id
    )
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        "single_list.html",
        {
            "post": post,
            "form": form,
            "comments": comments,
            "similar_posts": similar_posts,
        },
    )


# Create your views here.


def post_share(request, id):
    post = get_object_or_404(Post, id=id, status="PS")
    sent = False
    if request.method == "POST":
        form = ShareForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['username']} reommneds ou to read {post.title}"
            message = f"check out this post:{post_url}"
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[cd["to"]],
                from_email=None,
            )
            sent = True

    else:
        form = ShareForm()
    return render(request, "share.html", {"post": post, "form": form, "sent": sent})


def comment_view(request, id):
    post = get_object_or_404(Post, id=id, status="PS")
    comment = None
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return render(
        request, "comment.html", {"post": post, "comment": comment, "form": form}
    )


def searchform(request):
    query = None
    results = []
    form = SearchForm()
    print(query)
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "body", weight="B"
            )
            search_query = SearchQuery(query)
            search_rank = SearchRank(search_vector, search_query)
            similarity = TrigramSimilarity("title", query)
            results = (
                Post.objects.annotate(similarity=similarity)
                .filter(similarity__gte=0.1)
                .order_by("-similarity")
            )

    return render(
        request, "search.html", {"query": query, "form": form, "results": results}
    )


class PostlistView(ListView):
    queryset = Post.objects.filter(status="PS")
    context_object_name = "posts"
    paginate_by = 3
    template_name = "post_list.html"
