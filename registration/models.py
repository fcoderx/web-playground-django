from django.db import models 
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Guardar la última imagen del avatar
def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relación 1 a 1
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['user__username']



@receiver(post_save, sender=User) # Decorador para mandar las señales
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False): # Solo se mostrará la primera vez que se crea la instancia
        Profile.objects.get_or_create(user=instance)
        print("Se acaba de crear un usuario y su perfil enlazado")