from django.db import models

# Create your models here.

class Recipe (models.Model):
    title = models.CharField(max_length=150, unique=True)
    instructions = models.TextField()
    image = models.ImageField(upload_to='cookbook/images/', blank=True)
    ingredients = models.JSONField()

    def __str__(self):
        return self.title