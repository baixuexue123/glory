from django.contrib import admin
from .models import Tag, Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'is_active', 'author')
    list_filter = ('is_active',)
    exclude = ('body_html',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
