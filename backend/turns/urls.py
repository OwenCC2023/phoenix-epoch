from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.TurnListView.as_view(),
        name="turn-list",
    ),
    path(
        "current/",
        views.CurrentTurnView.as_view(),
        name="current-turn",
    ),
    path(
        "current/orders/",
        views.OrderListCreateView.as_view(),
        name="order-list-create",
    ),
    path(
        "current/submit/",
        views.SubmitOrdersView.as_view(),
        name="submit-orders",
    ),
    path(
        "<int:turn_number>/",
        views.TurnHistoryDetailView.as_view(),
        name="turn-history-detail",
    ),
]
