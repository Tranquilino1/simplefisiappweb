from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/default.png')
    theme_preference = models.CharField(max_length=20, default='dark', choices=[('dark', 'Dark'), ('light', 'Light')])
    status_message = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
