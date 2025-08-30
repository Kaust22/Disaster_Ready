from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Education modules
    path('module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('module/<int:module_id>/complete/', views.complete_module, name='complete_module'),
    
    # Quizzes
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    
    # Drills
    path('drill/<int:drill_id>/', views.drill_checklist, name='drill_checklist'),
    path('drill/<int:drill_id>/complete/', views.complete_drill, name='complete_drill'),
    
    # Emergency contacts
    path('emergency-contacts/', views.emergency_contacts, name='emergency_contacts'),
    
    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # API endpoints
    path('api/progress/<int:disaster_id>/', views.get_progress, name='get_progress'),
]
