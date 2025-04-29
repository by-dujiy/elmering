from django.contrib import admin
from .models import Words_Collection, Foreign_Word, Translate_Word


@admin.register(Translate_Word)
class Translate_WordAdmin(admin.ModelAdmin):
    list_display = ["word", "foreign_word"]


@admin.register(Foreign_Word)
class Foreign_WordAdmin(admin.ModelAdmin):
    list_display = ["word", "words_collection"]


@admin.register(Words_Collection)
class Words_CollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("collection_name",)}
    list_display = ["collection_name", "create_date", "slug"]
    search_fields = ["collection_name"]
