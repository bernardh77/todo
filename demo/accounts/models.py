from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_mod = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class ModProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme = models.CharField(
        max_length=10, 
        choices=[("light", "Light"), ("dark", "Dark")], 
        default="light"
    )

    def __str__(self):
        return f"{self.user.username} - {self.theme}"