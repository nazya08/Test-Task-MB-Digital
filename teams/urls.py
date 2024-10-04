from django.urls import path, include
from rest_framework.routers import DefaultRouter

from teams.views import teams, members

router = DefaultRouter()

# router.register(r'(?P<pk>\d+)/members', members.MemberView, 'members')
router.register(r'', teams.TeamView, 'teams')
router.register(r'(?P<team_id>\d+)/members', members.MemberView, 'members')

urlpatterns = [
    path('teams/', include(router.urls)),
    path('teams/search/', teams.TeamSearchView.as_view(), name='teams-search'),

]

