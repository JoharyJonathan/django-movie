from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def user_list(request):
    users = User.objects.all().order_by('id')
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admins/users.html', {'page_obj': page_obj})