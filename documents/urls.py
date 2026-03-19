from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='list'),
    path('contracts/<int:reservation_id>/print/', views.contract_print, name='contract_print'),
    path('contracts/<int:reservation_id>/print-ha/', views.contract_print_ha, name='contract_print_ha'),
    path('contracts/<int:reservation_id>/rules/', views.rules_print, name='rules_print'),
    path('contracts/<int:reservation_id>/pet-rules/', views.pet_rules_print, name='pet_rules_print'),
    path('contracts/<int:reservation_id>/email/', views.email_generator, name='email_generator'),
]
