from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def user_list(request):
    users = User.objects.all()
    user_count = users.count()
    
    return render(request, 'admins/users.html', {'users': users, 'user_count': user_count})