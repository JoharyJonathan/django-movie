from django.contrib.auth.models import User
from .models import Admin, Role

def create_admin(username, password, email, role_name):
    # Créer un utilisateur
    user = User.objects.create_user(username=username, password=password, email=email)
    
    # Associer un rôle à l'admin
    role = Role.objects.get(role_name=role_name)

    # Créer le profil Admin et l'associer à l'utilisateur
    admin = Admin.objects.create(user=user, role=role)

    return admin