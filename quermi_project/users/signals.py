from stripe import Customer
from stripe.error import InvalidRequestError

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import QuermiProfileUser
from utils.file_operations import remove_object, find_object_from_media


def remove_linked_payments(model_instance):
    if model_instance.customer_payment_id:
        try:
            payment_customer = Customer(
                model_instance.customer_payment_id)
            payment_customer.delete()
        except InvalidRequestError:
            pass

def remove_profile_assets(model_instance):
    id_photo_name = '{}_id_photo'.format(model_instance.pk)
    profile_photo_name = '{}_profile_photo'.format(model_instance.pk)
    
    id_photo_obj = find_object_from_media(id_photo_name)
    profile_photo_obj = find_object_from_media(profile_photo_name)

    remove_object(id_photo_obj)
    remove_object(profile_photo_obj)

@receiver(pre_delete, sender=QuermiProfileUser)
def tear_down_linked_data_on_profile(sender, **kwargs):
    model_instance = kwargs['instance']
    remove_linked_payments(model_instance)
    remove_profile_assets(model_instance)
