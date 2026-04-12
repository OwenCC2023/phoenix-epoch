"""Trade system URL configuration."""

from django.urls import path
from . import views

urlpatterns = [
    path("routes/", views.TradeRouteListView.as_view(), name="trade-route-list"),
    path("routes/<int:pk>/", views.TradeRouteDetailView.as_view(), name="trade-route-detail"),
    path("preview/", views.TradeRoutePreviewView.as_view(), name="trade-route-preview"),
    path("capacity/", views.TradeCapacityView.as_view(), name="trade-capacity"),
    path("capital-relocation/", views.CapitalRelocationView.as_view(), name="trade-capital-relocation"),
]
