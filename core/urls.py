from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('cadastro/', views.cadastro_cliente_view, name='cadastro_cliente'),
    path('cadastro-pet/', views.cadastro_pet_view, name='cadastro_pet'),
    path('agendar/', views.agendamento_view, name='agendamento'),
    path('historico/', views.historico_view, name='historico'),
]