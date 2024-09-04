import uuid

from django.db import models

HTML = "html"
TEXT = "text"


class Translation(models.Model):
    translation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user_id = models.UUIDField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    original_content = models.TextField(null=False)
    translated_content = models.TextField(null=False)

    FORMAT_CHOICES = [
        (HTML, "HTML"),
        (TEXT, "Text"),
    ]

    format = models.CharField(
        max_length=4, choices=FORMAT_CHOICES, default=TEXT, null=False
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(format__in=[HTML, TEXT]), name="format_valid"
            ),
        ]

    def __str__(self) -> str:
        return f"Translation {self.translation_id} for User {self.user_id}"
