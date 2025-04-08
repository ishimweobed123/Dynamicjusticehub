from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Location, User
from .forms import UserForm

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})

@require_http_methods(["POST"])
def user_create(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save()
        return JsonResponse({
            'success': True,
            'message': 'User created successfully'
        })
    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=user.id)
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'user': user})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

def get_parent_id(location_id):
    str_id = str(location_id)
    if location_id == 0:
        return None  # Country has no parent
    return int(str_id[:-2]) if len(str_id) > 2 else 0

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
            locations = locations.filter(location_id__gte=int(str(parent_id) + '1'), 
                                      location_id__lte=int(str(parent_id) + '9'))
        elif location_type.upper() == 'SECTOR':
            # Sectors start with the district ID
            locations = locations.filter(location_id__gte=int(str(parent_id) + '01'), 
                                      location_id__lte=int(str(parent_id) + '99'))
        elif location_type.upper() == 'CELL':
            # Cells start with the sector ID
            locations = locations.filter(location_id__gte=int(str(parent_id) + '01'), 
                                      location_id__lte=int(str(parent_id) + '99'))
    
    data = [{'id': loc.location_id, 'name': loc.name} for loc in locations]
    return JsonResponse(data, safe=False)

def get_location_hierarchy(location_id):
    """Get the full hierarchy of a location"""
    if not location_id:
        return None
    
    location = Location.objects.get(location_id=location_id)
    hierarchy = {
        'cell': None,
        'sector': None,
        'district': None,
        'province': None,
        'country': None
    }
    
    # Set the current level
    if location.type == 'CELL':
        hierarchy['cell'] = location
        parent_id = get_parent_id(location_id)
        if parent_id:
            hierarchy['sector'] = Location.objects.get(location_id=parent_id)
            parent_id = get_parent_id(parent_id)
            if parent_id:
                hierarchy['district'] = Location.objects.get(location_id=parent_id)
                parent_id = get_parent_id(parent_id)
                if parent_id:
                    hierarchy['province'] = Location.objects.get(location_id=parent_id)
                    hierarchy['country'] = Location.objects.get(location_id=0)
    elif location.type == 'SECTOR':
        hierarchy['sector'] = location
        parent_id = get_parent_id(location_id)
        if parent_id:
            hierarchy['district'] = Location.objects.get(location_id=parent_id)
            parent_id = get_parent_id(parent_id)
            if parent_id:
                hierarchy['province'] = Location.objects.get(location_id=parent_id)
                hierarchy['country'] = Location.objects.get(location_id=0)
    elif location.type == 'DISTRICT':
        hierarchy['district'] = location
        parent_id = get_parent_id(location_id)
        if parent_id:
            hierarchy['province'] = Location.objects.get(location_id=parent_id)
            hierarchy['country'] = Location.objects.get(location_id=0)
    elif location.type == 'PROVINCE':
        hierarchy['province'] = location
        hierarchy['country'] = Location.objects.get(location_id=0)
    
    return JsonResponse(hierarchy)

def get_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    return JsonResponse({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'sex': user.sex,
        'location': user.location.location_id if user.location else None
    })