from django.contrib import admin

from .models import CollectionType


class CollectionTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    search_fields = ["name"]

    class Meta:
        model = CollectionType

admin.site.register(CollectionType, CollectionTypeAdmin)

