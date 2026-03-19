from django.urls import path
from . import views

app_name = 'issues'

urlpatterns = [
    path('', views.issue_list, name='list'),
    path('new/', views.issue_new, name='new'),
    path('<int:pk>/edit/', views.issue_edit, name='edit'),
    path('<int:pk>/complete/', views.issue_complete, name='complete'),
    path('<int:pk>/delete/', views.issue_delete, name='delete'),
]
