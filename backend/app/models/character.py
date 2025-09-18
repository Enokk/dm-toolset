import os
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

def character_image_path(instance, filename):
    '''Generate file path for character images'''
    ext = filename.split('.')[-1]
    filename = f'character_{str(instance.pk) + '_' if instance.pk else ''}{instance.name.replace(' ', '_').lower()}'
    return os.path.join('characters', f'{filename}.{ext}')

class Character(models.Model):
    name = models.CharField(max_length=100)
    character_class = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    image = models.ImageField(upload_to=character_image_path, blank=True, null=True)
    hit_points = models.IntegerField()
    armor_class = models.IntegerField()
    
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    
    arcana = models.IntegerField(default=0)
    history = models.IntegerField(default=0)
    insight = models.IntegerField(default=0)
    investigation = models.IntegerField(default=0)
    nature = models.IntegerField(default=0)
    perception = models.IntegerField(default=0)
    religion = models.IntegerField(default=0)
    sleight_of_hand = models.IntegerField(default=0)
    stealth = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.character_class} {self.level}'
    
    @property
    def stats(self):
        '''Returns the stats as a dictionary'''
        return {
            'STR': self.strength,
            'DES': self.dexterity,
            'COS': self.constitution,
            'INT': self.intelligence,
            'SAG': self.wisdom,
            'CAR': self.charisma,
        }
    
    @property
    def skills(self):
        '''Returns the skills as a dictionary'''
        return {
            'arcano': self.arcana,
            'storia': self.history,
            'intuizione': self.insight,
            'indagare': self.investigation,
            'natura': self.nature,
            'percezione': self.perception,
            'religione': self.religion,
            'rapidità di mano': self.sleight_of_hand,
            'furtività': self.stealth,
        }

@receiver(pre_save, sender=Character)
def delete_old_image_on_update(sender, instance, **kwargs):
    '''Delete old image when updating with a new one'''
    if not instance.pk:
        return False
    
    try:
        old_file = Character.objects.get(pk=instance.pk).image
        new_file = instance.image
        
        if old_file and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except Character.DoesNotExist:
        return False

@receiver(post_delete, sender=Character)
def delete_image_on_delete(sender, instance, **kwargs):
    '''Delete image file when character is deleted'''
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


__all__ = ['Character']