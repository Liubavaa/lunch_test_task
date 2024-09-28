from django.urls import path
from . import views

urlpatterns = [
    path('api/restaurant/create/', views.create_restaurant, name='create-restaurant'),
    path('api/menu/upload/', views.upload_menu, name='upload-menu'),
    path('api/menu/today/', views.get_today_menu, name='get-today-menu'),
    path('api/menu/vote/', views.vote_for_menu, name='vote-menu'),
    path('api/menu/results/', views.get_results, name='get-menu-results'),
    path('api/employee/register/', views.RegisterEmployeeView.as_view(), name='register-employee'),
]