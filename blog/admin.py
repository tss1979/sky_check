from gettext import Catalog

from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content',)
    list_filter = ('title',)
    search_fields = ('title', 'content',)


