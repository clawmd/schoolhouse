from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.task_list, name='list'),
    path('new/', views.task_new, name='new'),
    path('<int:pk>/edit/', views.task_edit, name='edit'),
    path('<int:pk>/complete/', views.task_complete, name='complete'),
    path('<int:pk>/delete/', views.task_delete, name='delete'),
]
