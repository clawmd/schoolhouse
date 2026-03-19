from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('reservations:list'), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('guests/', include('guests.urls')),
    path('reservations/', include('reservations.urls')),
    path('expenses/', include('expenses.urls')),
    path('contacts/', include('contacts.urls')),
    path('documents/', include('documents.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('issues/', include('issues.urls')),
    path('reporting/', include('reporting.urls')),
    path('settings/', include('core.urls')),
    path('calendar/', include('reservations.calendar_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
