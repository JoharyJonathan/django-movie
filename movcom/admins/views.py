from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def user_list(request):
    users = User.objects.all().order_by('id')
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admins/users.html', {'page_obj': page_obj})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    return render(request, 'admins/user-detail.html', {'user': user})