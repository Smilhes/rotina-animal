from django.contrib import admin
from .models import Cliente, Pet

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
