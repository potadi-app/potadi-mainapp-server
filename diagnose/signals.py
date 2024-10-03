import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Diagnose

@receiver(pre_delete, sender=Diagnose)
def delete_image_on_destroy(sender, instance, **kwargs):
    if instance.image:
        if os.path.exists(instance.image.path):
            os.remove(instance.image.path)