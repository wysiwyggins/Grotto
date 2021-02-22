from django.contrib import admin
from characterBuilder.models import Character, CharacterTest, CharacterTestChoice


class CharacterTestChoiceInline(admin.StackedInline):
    model = CharacterTestChoice


@admin.register(CharacterTest)
class CharacterTestAdmin(admin.ModelAdmin):
    list_display = ("question",)
    inlines = (CharacterTestChoiceInline,)


admin.site.register(Character)
