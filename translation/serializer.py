from rest_framework import serializers

from translation.enums import FormatType
from translation.models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Translation' model
    """

    class Meta:
        model = Translation
        fields = [
            "translation_id",
            "user_id",
            "created_at",
            "format",
            "original_content",
            "translated_content",
        ]


class TranslationInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)
    format = serializers.ChoiceField(choices=[FormatType.TEXT.value, FormatType.HTML.value], required=True)
    original_content = serializers.CharField(required=True)
