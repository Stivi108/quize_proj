from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.CharField(max_length=42, null=True)
    teamLead = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
