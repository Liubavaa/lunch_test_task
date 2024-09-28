from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),

    path('restaurant/create/', views.create_restaurant, name='create-restaurant'),
    path('menu/upload/', views.upload_menu, name='upload-menu'),
    path('menu/today/', views.get_today_menu, name='get-today-menu'),
    path('menu/vote/<int:menu_id>', views.vote_for_menu, name='vote-menu'),
    path('menu/results/', views.get_results, name='get-menu-results'),
]
