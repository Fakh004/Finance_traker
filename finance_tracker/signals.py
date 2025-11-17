from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Balance, UserProfile


# i maqsad vaqte ki profile sozdat mekni avtomaticheske sozdalis BALANCE i USERPROFILE
@receiver(post_save, sender=CustomUser)
def create_user_related_objects(sender, instance, created, **kwargs):
    if created:
        # balance mesozem
        Balance.objects.create(user=instance, amount=0)
        # profile mesozem
        UserProfile.objects.create(user=instance)
