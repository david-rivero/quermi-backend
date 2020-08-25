from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import QuermiProfileUser
from utils.file_operations import remove_object, find_object_from_media


@receiver(pre_delete, sender=QuermiProfileUser)
def remove_profile_assets(sender, **kwargs):
    model_instance = kwargs['instance']
    id_photo_name = '{}_id_photo'.format(model_instance.pk)
    profile_photo_name = '{}_profile_photo'.format(model_instance.pk)
    
    id_photo_obj = find_object_from_media(id_photo_name)
    profile_photo_obj = find_object_from_media(profile_photo_name)

    remove_object(id_photo_obj)
    remove_object(profile_photo_obj)
