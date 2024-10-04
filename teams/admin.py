"""
AdminPanel for the teams app.
"""
from django.contrib import admin
from .models import Team, Member


class MemberInline(admin.TabularInline):
    model = Member
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    inlines = (MemberInline,)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'joined_at')
    list_filter = ('team',)
    search_fields = ('user__username', 'team__name')
