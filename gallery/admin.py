from django.contrib import admin
from django.utils import timezone

from .models import Image, ImageGroup


class ImageGroupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Date information", {"fields": ["publication_date"]}),
    ]
    list_display = ["id", "name", "publication_date", "days_since_published"]
    search_fields = ["name"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ImageGroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['publication_date'].initial = timezone.now()
        return form


class ImageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "description"]}),
        ("Image group", {"fields": ["group"]}),
        ("Images", {"fields": ["image_original", "image_thumbnail"]}),
        ("Date information", {"fields": ["publication_date"]}),
    ]
    list_display = ["id", "title", "description", "publication_date", "was_published_recently"]
    search_fields = ["title"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ImageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['publication_date'].initial = timezone.now()
        return form


admin.site.register(ImageGroup, ImageGroupAdmin)
admin.site.register(Image, ImageAdmin)
