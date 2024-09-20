from django.contrib import admin

from .models import *
from django.utils.text import slugify
# Register your models here.

admin.site.register(Question)
admin.site.register(Answers)


class GameListAdmin(admin.ModelAdmin):
    prepopulated_fields = {"RLSlug": ("gameNAME",)}
    list_display = ('__str__', 'RLSlug', 'status', 'winner')


admin.site.register(GameList, GameListAdmin)


@admin.register(RoundList)
class RoundListAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'gameName', 'team', 'round', 'team_answer', 'mark')



@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'game', 'team', 'current_round', 'score')



@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'game', 'round', 'question')


@admin.register(TeamList)
class TeamListAdmin(admin.ModelAdmin):
    list_display = ("team", "get_member")

    def get_member(self, obj):
        return [m.user for m in obj.member.all()]
