from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('home/', views.home, name='home'),
    path('add_student/', views.add_student, name='add_student'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('logout/', views.logout_view, name='logout'),
]