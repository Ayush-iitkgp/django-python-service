import logging
from typing import List

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework_api_key.permissions import HasAPIKey

from translation.models import Translation
from translation.serializer import TranslationSerializer

logger = logging.getLogger(__name__)


class UserTranslationsView(ListAPIView):
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
