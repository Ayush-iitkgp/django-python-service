import logging
from typing import Any

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from translation.enums import FormatType
from translation.models import Translation
from translation.serializer import TranslationInputSerializer
from translation.services.html_translation_service import HTMLTranslationService
from translation.services.translation_service import TranslationService

logger = logging.getLogger(__name__)


class TranslationView(APIView):
    permission_classes = [HasAPIKey]

    @staticmethod
    def post(request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = TranslationInputSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        logger.info(f"Translation POST request: {serializer.data}")

        validated_data = serializer.validated_data
        user_id = validated_data["user_id"]
        format = validated_data["format"]
        original_content = validated_data["original_content"]

        translated_content = None
        if format == FormatType.TEXT.value:
            translated_content = TranslationService.translate_text(original_content)
        else:
            translated_content = HTMLTranslationService.translate_html(original_content)

        # Save the translation in the database
        _ = Translation.objects.create(
            user_id=user_id, original_content=original_content, translated_content=translated_content, format=format
        )

        # Return the translation as a response
        response_data = {
            "user_id": user_id,
            "original_content": original_content,
            "translated_content": translated_content,
            "format": format,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
