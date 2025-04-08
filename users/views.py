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
        # Convert parent_id to integer
        parent_id = int(parent_id)
        
        # Filter based on location hierarchy
        if location_type.upper() == 'PROVINCE':
            # Provinces have IDs 1-5
            locations = locations.filter(location_id__gte=1, location_id__lte=5)
        elif location_type.upper() == 'DISTRICT':
            # Districts start with the province number
            province_prefix = str(parent_id)
            locations = locations.filter(location_id__gte=int(province_prefix + '1'), 
                                      location_id__lte=int(province_prefix + '9'))
        elif location_type.upper() == 'SECTOR':
            # Sectors start with the district ID
            district_prefix = str(parent_id)
            locations = locations.filter(location_id__gte=int(district_prefix + '01'), 
                                      location_id__lte=int(district_prefix + '99'))
        elif location_type.upper() == 'CELL':
            # Cells start with the sector ID
            sector_prefix = str(parent_id)
            locations = locations.filter(location_id__gte=int(sector_prefix + '01'), 
                                      location_id__lte=int(sector_prefix + '99'))
    
    data = [{'id': loc.location_id, 'name': loc.name} for loc in locations]
    return JsonResponse(data, safe=False)