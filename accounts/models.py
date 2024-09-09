from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    REGISTRATION_CHOICES = [
        ('email', 'Email'),
        ('google', 'Google'),
    ]
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email'
    )
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
