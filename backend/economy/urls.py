from django.urls import path

from . import views

urlpatterns = [
    path(
        "nations/<int:nation_id>/construction/",
        views.NationConstructionView.as_view(),
        name="nation-construction",
    ),
    path(
        "nations/<int:nation_id>/goods/",
        views.NationGoodStockView.as_view(),
        name="nation-good-stock",
    ),
    path(
        "nations/<int:nation_id>/resources/",
        views.NationResourcePoolView.as_view(),
        name="nation-resource-pool",
    ),
    path(
        "nations/<int:nation_id>/ledger/",
        views.ResourceLedgerListView.as_view(),
        name="resource-ledger-list",
    ),
    path(
        "trades/",
        views.TradeOfferListCreateView.as_view(),
        name="trade-offer-list-create",
    ),
    path(
        "trades/<int:pk>/respond/",
        views.TradeOfferResponseView.as_view(),
        name="trade-offer-respond",
    ),
]
