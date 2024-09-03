from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, related_name='admins')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_last_login(self):
        self.user.last_login = timezone.now()
        self.user.save()
        
    def __str__(self):
        return self.user.username
    
class Role(models.Model):
    role_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField('Permission', related_name='roles')
    
    def __str__(self):
        return self.role_name
    
class Permission(models.Model):
    permission_name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100, unique=True, help_text="unique code for the permission")
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.permission_name
    
class AdminAction(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    target_status_before = models.TextField(blank=True, null=True)
    target_status_after = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.admin.user.username} performed {self.action_type} on {self.content_object} at {self.timestamp}"