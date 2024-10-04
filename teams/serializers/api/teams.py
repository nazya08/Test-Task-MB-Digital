from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from teams.models import Team, Member
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class TeamSearchListSerializer(serializers.ModelSerializer):
    team_leader = UserShortSerializer()

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'team_leader',
        )


class TeamListRetrieveSerializer(serializers.ModelSerializer):
    team_leader = UserShortSerializer()
    members_count = serializers.IntegerField()

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'team_leader',
            'members_count',
            'created_at',
        )


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'id',
            'name',
        )

    def validate_name(self, value):
        if self.Meta.model.objects.filter(name=value).exists():
            raise ParseError(
                'Team with this name already exists.'
            )
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        with transaction.atomic():
            team = Team.objects.create(name=validated_data['name'], team_leader=user)
            Member.objects.create(user=user, team=team)
        return team


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'id',
            'name',
        )
