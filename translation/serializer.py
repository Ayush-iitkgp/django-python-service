from rest_framework import serializers

from translation.models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Translation' model
    """

    first_question = serializers.SerializerMethodField(allow_null=True)
    total_questions = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Translation
        fields = [
            "id",
            "project",
            "created_at",
            "first_question",
            "total_questions",
            "label",
        ]
