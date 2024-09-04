from rest_framework import serializers

from translation.models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Translation' model
    """

    user_id = serializers.UUIDField(allow_null=False)

    class Meta:
        model = Translation
        fields = [
            "translation_id",
            "created_at",
            "format",
            "original_content",
            "translated_content",
        ]
