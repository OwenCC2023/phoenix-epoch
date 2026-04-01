"""Espionage system URL configuration."""

from django.urls import path
from . import views

urlpatterns = [
    path("overview/", views.EspionageOverviewView.as_view(), name="espionage-overview"),
    path(
        "targets/<int:target_nation_id>/",
        views.EspionageTargetDetailView.as_view(),
        name="espionage-target-detail",
    ),
    path("sharing/", views.IntelligenceSharingView.as_view(), name="intelligence-sharing"),
    path("actions/", views.EspionageActionListView.as_view(), name="espionage-actions"),
    path("slots/", views.EspionageSlotView.as_view(), name="espionage-slots"),
]
