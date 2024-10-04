from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.viewsets import ModelViewSet

from teams.models import Member
from teams.serializers.api import members


@extend_schema_view(
    list=extend_schema(summary='List of team members', tags=['Teams: Members']),
    retrieve=extend_schema(summary='Team Member Detail', tags=['Teams: Members']),
    create=extend_schema(summary='Create team member', tags=['Teams: Members']),
    update=extend_schema(summary='Update team member', tags=['Teams: Members']),
    partial_update=extend_schema(summary='Update team member partially', tags=['Teams: Members']),
    destroy=extend_schema(summary='Delete member from team', tags=['Teams: Members']),
    search=extend_schema(filters=True, summary='List of team members Search', tags=['Teams: Members']),
)
class MemberView(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = members.MemberListRetrieveSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return members.MemberCreateSerializer
        elif self.request.method in ('PUT', 'PATCH',):
            return members.MemberUpdateSerializer
        elif self.request.method == 'DELETE':
            return members.MemberDeleteSerializer
        return self.serializer_class

    lookup_url_kwarg = 'member_id'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering = ('joined_at', 'id',)

    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        return Member.objects.select_related('user').prefetch_related('team').filter(team_id=team_id)

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=dict())
        serializer.is_valid(raise_exception=True)
        return super().destroy(request, *args, **kwargs)
