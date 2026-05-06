from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_staff_warung = models.BooleanField(default=True)