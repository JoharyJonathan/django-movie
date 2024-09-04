from django.shortcuts import render, get_object_or_404, redirect
from .models import Actor
from .forms import ActorForm

# Create your views here.
def actor_create(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('actor_list')
    else:
        form = ActorForm()
        
    return render(request, 'actors/actor_form.html', {'form': form})
    
def actor_list(request):
    actors = Actor.objects.all()
    
    return render(request, 'actors/actor_list.html', {'actors': actors})

def actor_update(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    if request.method == 'POST':
        form = ActorForm(request.POST, instance=actor)
        if form.is_valid():
            form.save()
            return redirect('actor_list.html')
    else:
        form = ActorForm(instance=actor)
        
    return render(request, 'actors/actor_form.html', {'form': form})

def actor_delete(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    if request.method == 'POST':
        actor.delete()
        return redirect('actor_list')
    
    return render(request, 'actors/actor_confirm_delete.html', {'actor': actor})