from django.urls import path
from core.views import chat_view

urlpatterns = [
    path("", chat_view, name="chat"),
]
