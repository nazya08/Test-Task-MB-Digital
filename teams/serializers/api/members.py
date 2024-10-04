from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from teams.models import Member, Team
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class MemberSearchSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'user',
        )


class MemberListRetrieveSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Member
        fields = (
            'id',
            'joined_at',
            'user',
        )


class MemberCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        )

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                'User with this email already exists.'
            )
        return email

    def validate_username(self, value):
        username = value
        if User.objects.filter(username=username).exists():
            raise ParseError(
                'User with this username already exists.'
            )
        return username

    def validate(self, attrs):
        current_user = self.context['request'].user

        team_id = self.context['view'].kwargs.get('team_id')
        team = Team.objects.filter(
            id=team_id, team_leader=current_user,
        ).first()

        if not team:
            raise ParseError(
                'Team not found.'
            )

        attrs['team'] = team

        return attrs

    def create(self, validated_data):
        user_data = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'email': validated_data.pop('email'),
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
        }

        with transaction.atomic():
            user = User.objects.create_user(**user_data)
            validated_data['user'] = user

            instance = super().create(validated_data)
        return instance


class MemberUpdateSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all()
    )

    class Meta:
        model = Member
        fields = ('team',)

    def validate(self, attrs):
        if self.instance.is_team_leader:
            raise ParseError(
                'Team leader can not be changed.'
            )
        return attrs


class MemberDeleteSerializer(serializers.Serializer):
    def validate(self, attrs):
        if self.instance.is_team_leader:
            raise ParseError(
                'Can not delete team leader.'
            )

        return attrs
