from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter, BaseFilterBackend
from rest_framework.viewsets import ModelViewSet

from teams.models import Team
from teams.permissions import IsMyTeam
from teams.serializers.api import teams


class MyTeam(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(
            Q(team_leader=user) | Q(members=user)
        ).distinct()


@extend_schema_view(
    list=extend_schema(summary='List of teams Search', tags=['Teams']),
)
class TeamSearchView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = teams.TeamSearchListSerializer


@extend_schema_view(
    list=extend_schema(summary='List of teams', tags=['Teams']),
    retrieve=extend_schema(summary='Team Detail', tags=['Teams']),
    create=extend_schema(summary='Create Team', tags=['Teams']),
    update=extend_schema(summary='Update Team', tags=['Teams']),
    partial_update=extend_schema(summary='Update Team Partially', tags=['Teams']),
)
class TeamView(ModelViewSet):
    permission_classes = [IsMyTeam]
    queryset = Team.objects.all()
    serializer_class = teams.TeamListRetrieveSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return teams.TeamCreateSerializer
        elif self.request.method in ('PUT', 'PATCH',):
            return teams.TeamUpdateSerializer
        return teams.TeamListRetrieveSerializer

    http_method_names = ('get', 'post', 'patch')

    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
        MyTeam,
    )
    ordering = ('name', 'id',)

    def get_queryset(self):
        return Team.objects.select_related(
            'team_leader',
        ).prefetch_related(
            'members',
        ).annotate(
            members_count=Count('members', distinct=True),
        )
