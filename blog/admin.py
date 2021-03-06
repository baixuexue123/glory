from django.contrib import admin
from .models import Tag, Category, Post, Comment


admin.site.register(Tag)
admin.site.register(Category)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'is_active', 'is_published', 'author')
    list_filter = ('is_active',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'body':
            formfield.widget.attrs.update({
                'rows': 32,
                'style': 'font-family: monospace; width: 810px;',
            })
        return formfield


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'ip_address', 'active', 'created')
    list_filter = ('active',)
