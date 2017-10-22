from django.contrib import admin
from django.forms.widgets import Textarea

from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('desc', 'pub_date', 'image')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'desc':
            kwargs['widget'] = Textarea
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        return formfield
