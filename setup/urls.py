# setup/urls.py
from django.contrib import admin
from django.urls import path
from core import views  # Importa as views que criamos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('cadastro/', views.cadastro_cliente_view, name='cadastro_cliente'),
    path('agendar/', views.agendamento_view, name='agendamento'),
    path('historico/', views.historico_view, name='historico'),
]