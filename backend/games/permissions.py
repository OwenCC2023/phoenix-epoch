from rest_framework.permissions import BasePermission

from .models import GameMembership


class IsGameCreator(BasePermission):
    """Only the game creator can perform this action."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsGameMember(BasePermission):
    """Only members of the game can perform this action."""

    def has_object_permission(self, request, view, obj):
        return GameMembership.objects.filter(game=obj, user=request.user).exists()
