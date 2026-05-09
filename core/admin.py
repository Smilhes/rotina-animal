from django.contrib import admin
from .models import Cliente, Pet, Agendamento

class PetInline(admin.TabularInline):
    model = Pet
    extra = 1

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'telefone', 'bairro', 'criado_em')
    search_fields = ('nome_cliente', 'telefone', 'cpf')
    inlines = [PetInline]

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('nome_pet', 'cliente', 'raca_pet', 'porte_pet')
    search_fields = ('nome_pet', 'cliente__nome_cliente')
    list_filter = ('porte_pet', 'cliente')

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('pet', 'cliente', 'data', 'hora_inicio', 'tipo_servico', 'status', 'pago')
    search_fields = ('pet__nome_pet', 'cliente__nome_cliente', 'tipo_servico')
    list_filter = ('status', 'pago', 'data', 'tipo_servico')
    date_hierarchy = 'data'
