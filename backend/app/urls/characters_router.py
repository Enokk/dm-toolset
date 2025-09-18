from django.shortcuts import get_object_or_404
from ninja import Router, ModelSchema
from typing import List

from ..models import Character

characters_router = Router()

class NinjaResponseCharacter(ModelSchema):
    # TODO: trova un modo per gestire in un unico posto questi due campi
    stats: dict
    skills: dict
    
    class Meta:
        model = Character
        fields = '__all__'


@characters_router.get('characters', response=List[NinjaResponseCharacter])
def get_characters(request):
    return Character.objects.all()

@characters_router.get('characters/{id}', response=NinjaResponseCharacter)
def get_character_by_id(request, id: int):
    return get_object_or_404(Character, id=id)    

__all__ = ['characters_router']