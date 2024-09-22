from django.db import models

# Create your models here.

class AppConfig(models.Model):
    allow_introspection = models.BooleanField(default=False)