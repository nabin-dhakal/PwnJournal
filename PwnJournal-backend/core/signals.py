import sys
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if 'makemigrations' in sys.argv or 'migrate' in sys.argv:
        return
    if created and not instance.is_staff:
        UserProfile.objects.create(user=instance)
