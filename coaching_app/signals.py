from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from . models import Coach, Student


@receiver(post_save, sender=User, dispatch_uid="create_user_profile")
def create_user_profile(sender, instance, **kwargs):
   print("**** signal received")
   print(sender)
   print(kwargs)
   if not Coach.objects.filter(user=instance).exists():
      coach = Coach()
      coach.user = instance
      coach.save()