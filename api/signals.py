from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import NewUser, Property

User = NewUser()

@receiver(pre_save, sender=Property)
def assign_user_to_property(request, sender, instance, **kwargs):
  if not instance.user:  # Check if user is not already set
    instance.user = User.objects.get(pk=request.user.pk)  # Replace with logic to get user

