from django.contrib import admin

from .models import NationGoodStock, NationResourcePool, ResourceLedger, ProvinceLedger, TradeOffer


@admin.register(NationGoodStock)
class NationGoodStockAdmin(admin.ModelAdmin):
    list_display = ("nation", "consumer_goods", "arms", "fuel", "machinery")
    search_fields = ("nation__name",)


@admin.register(NationResourcePool)
class NationResourcePoolAdmin(admin.ModelAdmin):
    list_display = ("nation", "food", "materials", "energy", "wealth", "manpower", "research", "stability", "total_population")
    search_fields = ("nation__name",)


@admin.register(ResourceLedger)
class ResourceLedgerAdmin(admin.ModelAdmin):
    list_display = ("nation", "turn_number", "created_at")
    list_filter = ("turn_number",)
    search_fields = ("nation__name",)


@admin.register(ProvinceLedger)
class ProvinceLedgerAdmin(admin.ModelAdmin):
    list_display = ("province", "turn_number", "population", "created_at")
    list_filter = ("turn_number",)
    search_fields = ("province__name",)


@admin.register(TradeOffer)
class TradeOfferAdmin(admin.ModelAdmin):
    list_display = ("from_nation", "to_nation", "turn_number", "status", "created_at")
    list_filter = ("status", "turn_number")
    search_fields = ("from_nation__name", "to_nation__name")
