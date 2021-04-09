from django.db import models
from django.contrib.auth.models import User
from cookbook.models import Recipe

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    savedCart = models.JSONField(blank=True, null=True)
    favorites = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return self.user.username + "'s profile"