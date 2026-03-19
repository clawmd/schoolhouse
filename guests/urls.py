from django.urls import path
from . import views

app_name = 'guests'

urlpatterns = [
    path('', views.guest_list, name='list'),
    path('new/', views.guest_new, name='new'),
    path('search/', views.guest_search_htmx, name='search'),
    path('<int:pk>/', views.guest_detail, name='detail'),
    path('<int:pk>/edit/', views.guest_edit, name='edit'),
    path('<int:pk>/delete/', views.guest_delete, name='delete'),
]
