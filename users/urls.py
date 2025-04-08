from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('update/<int:pk>/', views.user_update, name='user_update'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('api/locations/<str:location_type>/', views.get_locations, name='get_locations'),
    path('api/locations/hierarchy/<int:location_id>/', views.get_location_hierarchy, name='get_location_hierarchy'),
    path('api/users/<int:pk>/', views.get_user, name='get_user'),
]
