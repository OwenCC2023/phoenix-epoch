from django.urls import path

from . import views

urlpatterns = [
    path("", views.GameListCreateView.as_view(), name="game-list-create"),
    path("<int:pk>/", views.GameDetailView.as_view(), name="game-detail"),
    path("<int:pk>/join/", views.GameJoinView.as_view(), name="game-join"),
    path("<int:pk>/leave/", views.GameLeaveView.as_view(), name="game-leave"),
    path("<int:pk>/start/", views.GameStartView.as_view(), name="game-start"),
    path("<int:pk>/members/", views.GameMembersView.as_view(), name="game-members"),
    path("<int:pk>/admin/pause/", views.GamePauseView.as_view(), name="game-pause"),
    path("<int:pk>/admin/resume/", views.GameResumeView.as_view(), name="game-resume"),
    path("<int:pk>/admin/force-resolve/", views.GameForceResolveView.as_view(), name="game-force-resolve"),
    path("<int:pk>/admin/overview/", views.GameAdminOverviewView.as_view(), name="game-admin-overview"),
]
