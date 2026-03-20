from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProvinceListView.as_view(), name="province-list"),
    path("<int:pk>/", views.ProvinceDetailView.as_view(), name="province-detail"),
    path("<int:pk>/allocations/", views.ProvinceAllocationView.as_view(), name="province-allocations"),
    path("<int:pk>/buildings/", views.BuildingView.as_view(), name="province-buildings"),
    path("zones/air/", views.AirZoneListView.as_view(), name="airzone-list"),
    path("zones/sea/", views.SeaZoneListView.as_view(), name="seazone-list"),
    path("zones/river/", views.RiverZoneListView.as_view(), name="riverzone-list"),
]
