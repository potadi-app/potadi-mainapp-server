from django.db import models
from uuid import uuid4

def user_directory_path(instance, filename):
    return f'diagnoses/{instance.user.email}/{filename}'

class Diagnose(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
    label = models.CharField(max_length=100)
    confidence = models.FloatField()
    detail = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.user.username} - [{self.user.email}]'