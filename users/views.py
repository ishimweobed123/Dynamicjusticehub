from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Location, User
from .forms import UserForm

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

def get_locations(request, location_type):
    parent_id = request.GET.get('parent')
    locations = Location.objects.filter(type=location_type.upper())
    if parent_id:
        locations = locations.filter(location_id__startswith=parent_id)  # Filtering logic
    data = [{'id': loc.location_id, 'name': loc.name} for loc in locations]
    return JsonResponse(data, safe=False)