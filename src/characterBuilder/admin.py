from django.contrib import admin

from characterBuilder.models import (
    Character,
    CharacterTest,
    CharacterTestChoice,
    NonPlayerCharacter,
    Visit,
)


class CharacterTestChoiceInline(admin.StackedInline):
    model = CharacterTestChoice


@admin.register(CharacterTest)
class CharacterTestAdmin(admin.ModelAdmin):
    list_display = ("question",)
    inlines = (CharacterTestChoiceInline,)


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("character", "room", "stamp_date")


@admin.register(NonPlayerCharacter)
class NonPlayerCharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "room", "mobile")

admin.site.register(Character)
