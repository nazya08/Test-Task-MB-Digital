from django.contrib.auth import get_user_model
from django.db import models

from common.models import TimeStampedModel

User = get_user_model()


class Team(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(
        User,
        related_name='teams',
        verbose_name='Members',
        blank=True,
        through='Member',
    )

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='team_members'
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='team_members'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        ordering = ('-joined_at',)
        unique_together = (('user', 'team'),)

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"
