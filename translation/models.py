import uuid

from django.db import models

from translation.enums import FormatType


class Translation(models.Model):
    translation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    original_content = models.TextField(null=False)
    translated_content = models.TextField(null=False)

    FORMAT_CHOICES = [
        (FormatType.HTML, "HTML"),
        (FormatType.TEXT, "Text"),
    ]

    format = models.CharField(max_length=4, choices=FORMAT_CHOICES, default=FormatType.TEXT, null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(format__in=[FormatType.HTML, FormatType.TEXT]), name="format_valid"),
        ]

    def __str__(self) -> str:
        return f"Translation {self.translation_id} for User {self.user_id}"
