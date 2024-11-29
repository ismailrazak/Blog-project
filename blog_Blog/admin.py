from django.contrib import admin

from .models import Comment, Post

# Register your models here.
admin.site.register(Comment)


@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    list_display = ["title", "slug", "created", "publish", "status"]
    list_filter = ["publish", "author", "slug"]
    raw_id_fields = ["author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish"
    ordering = ["publish", "status"]
    show_facets = admin.ShowFacets.ALWAYS
