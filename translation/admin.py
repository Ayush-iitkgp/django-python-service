from django.contrib import admin

from translation.models import Translation


@admin.register(Translation)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        "translation_id",
        "created_at",
        "user_id",
        "format",
        "original_content",
        "translated_content",
    )
    ordering = ("-created_at",)
