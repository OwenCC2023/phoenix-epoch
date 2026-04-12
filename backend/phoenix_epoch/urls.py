"""
URL configuration for Phoenix Epoch project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/games/", include("games.urls")),
    path("api/games/<int:game_id>/nations/", include("nations.urls")),
    path("api/games/<int:game_id>/provinces/", include("provinces.urls")),
    path("api/games/<int:game_id>/", include("economy.urls")),
    path("api/games/<int:game_id>/turns/", include("turns.urls")),
    path("api/games/<int:game_id>/", include("events.urls")),
    path("api/games/<int:game_id>/espionage/", include("espionage.urls")),
    path("api/games/<int:game_id>/trade/", include("trade.urls")),
]
