import logging

from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from translation.models import Translation
from translation.serializer import TranslationSerializer

logger = logging.getLogger(__name__)


class TranslateAndRetrieveAPIView(APIView):
    permission_classes = [HasAPIKey]
    serializer_class = TranslationSerializer
    http_method_names = ["get"]

    def get_queryset(self) -> models.QuerySet:
        user_id = self.kwargs.get("user_id")
        if user_id:
            _ = get_object_or_404(Translation, id=user_id)
            return Translation.objects.filter(user_id=user_id)
        raise ValidationError("User ID is required")
