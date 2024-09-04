import logging
from typing import Any, List

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from translation.models import Translation
from translation.serializer import TranslationInputSerializer, TranslationSerializer
from translation.services.translation_service import TranslationService

logger = logging.getLogger(__name__)


class TranslateAndRetrieveAPIView(ListAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = TranslationSerializer

    def get_queryset(self) -> List[Translation]:
        user_id = self.kwargs.get("user_id")
        if not user_id:
            raise ValidationError("user_id is required")

        translations = Translation.objects.filter(user_id=user_id)
        if len(translations) == 0:
            raise NotFound(f"No translation found for the user {user_id}")
        return translations

    @staticmethod
    def post(request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = TranslationInputSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        validated_data = serializer.validated_data
        user_id = validated_data["user_id"]
        format = validated_data["format"]
        original_content = validated_data["original_content"]

        translated_content = TranslationService.translate_text(original_content)

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
