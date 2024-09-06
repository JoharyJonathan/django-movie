from django.contrib.auth.models import User
from .models import Admin, Role

def create_admin(username, password, email, role_name='admin'):
    # Créer un utilisateur
    user = User.objects.create_user(username=username, password=password, email=email)
    
    # Chercher ou créer le rôle basé sur un nom de rôle par défaut
    role, created = Role.objects.get_or_create(role_name=role_name)
    if created:
        print(f"Rôle '{role_name}' créé car il n'existait pas.")

    # Créer le profil Admin et l'associer à l'utilisateur
    admin = Admin.objects.create(user=user, role=role)

    return admin