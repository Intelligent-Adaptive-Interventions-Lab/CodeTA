"""
URL mappings for the executor app.
"""
from django.urls import path, include

from executor import views

app_name = 'executor'

urlpatterns = [
    path('execute/', views.execute_code),
    path('get_executor/', views.get_code_executor),
]