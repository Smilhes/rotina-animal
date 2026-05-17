from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Clientes
    path('clientes/', views.cadastro_cliente_view, name='cadastro_cliente'),
    path('cliente/<int:cliente_id>/', views.cliente_detail_view, name='cliente_detail'),
    path('cliente/novo/', views.cliente_create_view, name='cliente_create'),
    path('cliente/<int:cliente_id>/editar/', views.cliente_edit_view, name='cliente_edit'),
    
    # Pets
    path('cliente/<int:cliente_id>/pet/novo/', views.pet_create_view, name='pet_create'),
    path('pet/<int:pet_id>/editar/', views.pet_edit_view, name='pet_edit'),
    path('pet/<int:pet_id>/deletar/', views.pet_delete_view, name='pet_delete'),
    
    path('agendar/', views.agendamento_view, name='agendamento'),
    path('historico/', views.historico_view, name='historico'),

    path('api/buscar-clientes/', views.api_buscar_clientes, name='api_buscar_clientes'),
    path('api/buscar-pets/<int:cliente_id>/', views.api_buscar_pets, name='api_buscar_pets'),
    path('api/agendamento/<int:agendamento_id>/iniciar/', views.api_iniciar_agendamento, name='api_iniciar_agendamento'),
    path('api/agendamento/<int:agendamento_id>/concluir/', views.api_concluir_agendamento, name='api_concluir_agendamento'),
]