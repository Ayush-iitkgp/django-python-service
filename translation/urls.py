from django.urls import path
from rest_framework.routers import DefaultRouter

from translation.views.translation import TranslateAndRetrieveAPIView

router = DefaultRouter()

urlpatterns = [
    path(
        "<uuid:user_id>/",
        TranslateAndRetrieveAPIView.as_view(
            {
                "get": "list",
            }
        ),
        name="users-list",
    ),
]
