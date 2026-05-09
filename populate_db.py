import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rotina_animal.settings')
django.setup()

from core.models import Cliente, Pet

# Limpar dados antigos
Pet.objects.all().delete()
Cliente.objects.all().delete()

# Criar clientes de exemplo
cliente1 = Cliente.objects.create(
    nome_cliente='João da Silva',
    telefone='(11) 98888-7777',
    cpf='123.456.789-00',
    rua='Avenida Paulista',
    numero='1000',
    bairro='Bela Vista'
)

cliente2 = Cliente.objects.create(
    nome_cliente='Maria Souza',
    telefone='(11) 99999-8888',
    cpf='987.654.321-00',
    rua='Rua Augusta',
    numero='500',
    bairro='Centro'
)

# Criar pets para o primeiro cliente
Pet.objects.create(
    cliente=cliente1,
    nome_pet='Thor',
    raca_pet='Golden Retriever',
    porte_pet='grande',
    idade_pet='3 anos'
)

Pet.objects.create(
    cliente=cliente1,
    nome_pet='Luna',
    raca_pet='Persa',
    porte_pet='pequeno',
    idade_pet='1 ano'
)

# Criar pets para o segundo cliente
Pet.objects.create(
    cliente=cliente2,
    nome_pet='Mel',
    raca_pet='Poodle',
    porte_pet='pequeno',
    idade_pet='2 anos'
)

Pet.objects.create(
    cliente=cliente2,
    nome_pet='Rex',
    raca_pet='SRD',
    porte_pet='medio',
    idade_pet='4 anos'
)

print("✓ Dados de exemplo criados com sucesso!")
print(f"  - {Cliente.objects.count()} clientes")
print(f"  - {Pet.objects.count()} pets")
