from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsMyTeam(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.team_leader == request.user:
            return True

        if request.method in SAFE_METHODS:
            return request.user in obj.members.all()

        return False
