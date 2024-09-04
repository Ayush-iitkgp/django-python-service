from django.urls import path
from rest_framework.routers import DefaultRouter

from translation.views.translate_retrieve_view import TranslateAndRetrieveAPIView

router = DefaultRouter()

urlpatterns = [
    path(
        "<uuid:user_id>",
        TranslateAndRetrieveAPIView.as_view(),
        name="translation-list",
    ),
    path(
        "translate",
        TranslateAndRetrieveAPIView.as_view(),
        name="translation-create",
    ),
]
