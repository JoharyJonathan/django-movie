from django.contrib import admin
from .models import Admin, Role, Permission, AdminAction

# Register your models here.
admin.site.register(Admin)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(AdminAction)