from django.contrib import admin

from .models import Character

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'character_class', 'level']
    list_filter = ['character_class']
    search_fields = ['name']
    
    fieldsets = (
        ('Informazioni Base', {
            'fields': ('name', 'character_class', 'level', 'image', 'hit_points', 'armor_class')
        }),
        ('Statistiche', {
            'fields': ('strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma'),
        }),
        ('Abilità', {
            'fields': ('arcana', 'history', 'insight', 'investigation', 'nature', 'perception', 'religion', 'sleight_of_hand', 'stealth'),
        }),
    )
