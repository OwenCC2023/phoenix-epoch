from django.contrib import admin

from .models import Turn, Order, TurnSubmission


@admin.register(Turn)
class TurnAdmin(admin.ModelAdmin):
    list_display = ["game", "turn_number", "status", "deadline", "started_at", "resolved_at"]
    list_filter = ["status", "game"]
    ordering = ["-started_at"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["turn", "nation", "order_type", "status", "created_at", "updated_at"]
    list_filter = ["order_type", "status"]
    ordering = ["-created_at"]


@admin.register(TurnSubmission)
class TurnSubmissionAdmin(admin.ModelAdmin):
    list_display = ["turn", "nation", "submitted_at"]
    ordering = ["-submitted_at"]
