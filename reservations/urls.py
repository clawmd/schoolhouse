from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='list'),
    path('new/', views.reservation_new, name='new'),
    path('calendar/', views.reservation_calendar, name='calendar'),
    path('rates/', views.rate_list, name='rate_list'),
    path('rates/new/', views.rate_new, name='rate_new'),
    path('rates/<int:pk>/edit/', views.rate_edit, name='rate_edit'),
    path('rates/<int:pk>/delete/', views.rate_delete, name='rate_delete'),
    path('<int:pk>/', views.reservation_detail, name='detail'),
    path('<int:pk>/edit/', views.reservation_edit, name='edit'),
    path('<int:pk>/delete/', views.reservation_delete, name='delete'),
]
