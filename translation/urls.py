from django.urls import path
from rest_framework.routers import DefaultRouter

from translation.views.translation_view import TranslationView
from translation.views.user_translations_view import UserTranslationsView

router = DefaultRouter()

urlpatterns = [
    path(
        "<uuid:user_id>",
        UserTranslationsView.as_view(),
        name="translation-list",
    ),
    path(
        "translate",
        TranslationView.as_view(),
        name="translation-create",
    ),
]
