from django.urls import path

from . import views

urlpatterns = [
    path("events/", views.GameEventListCreateView.as_view(), name="game-event-list-create"),
    path("events/templates/", views.EventTemplateListView.as_view(), name="event-template-list"),
]
