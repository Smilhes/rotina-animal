# Documentação Técnica - Sistema de Clientes e Pets

## Estrutura de URLs

### Clientes
```
GET  /clientes/                    - Lista todos os clientes
POST /clientes/                    - Não implementado (usar /cliente/novo/)
GET  /cliente/novo/                - Formulário para novo cliente
POST /cliente/novo/                - Salva novo cliente
GET  /cliente/<id>/                - Detalhes do cliente
GET  /cliente/<id>/editar/         - Formulário para editar cliente
POST /cliente/<id>/editar/         - Salva edições do cliente
```

### Pets
```
GET  /cliente/<id>/pet/novo/       - Formulário para novo pet
POST /cliente/<id>/pet/novo/       - Salva novo pet
GET  /pet/<id>/editar/             - Formulário para editar pet
POST /pet/<id>/editar/             - Salva edições do pet
POST /pet/<id>/deletar/            - Deleta pet (requer POST)
```

## Modelos de Dados

### Cliente
```python
class Cliente(models.Model):
    nome_cliente      - CharField(max_length=100)
    telefone          - CharField(max_length=20)
    cpf               - CharField(max_length=11, unique=True, null=True)
    rua               - CharField(max_length=100, null=True, blank=True)
    numero            - CharField(max_length=10, null=True, blank=True)
    bairro            - CharField(max_length=100, null=True, blank=True)
    criado_em         - DateTimeField(auto_now_add=True)
    atualizado_em     - DateTimeField(auto_now=True)
```

### Pet
```python
class Pet(models.Model):
    cliente           - ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pets')
    nome_pet          - CharField(max_length=100)
    raca_pet          - CharField(max_length=100)
    porte_pet         - CharField(max_length=20, choices=[
                          ('pequeno', 'Pequeno'),
                          ('medio', 'Médio'),
                          ('grande', 'Grande'),
                        ])
    idade_pet         - CharField(max_length=20, null=True, blank=True)
    criado_em         - DateTimeField(auto_now_add=True)
    atualizado_em     - DateTimeField(auto_now=True)
```

## Views

### cadastro_cliente_view(request)
- Método: GET
- Retorna lista de todos os clientes
- Template: `cadastro_cliente.html`

### cliente_detail_view(request, cliente_id)
- Método: GET
- Mostra detalhes de um cliente e seus pets
- Template: `cliente_detail.html`

### cliente_create_view(request)
- Método: GET/POST
- GET: Exibe formulário para novo cliente
- POST: Cria novo cliente e redireciona para detalhes
- Template: `cliente_form.html`

### cliente_edit_view(request, cliente_id)
- Método: GET/POST
- GET: Exibe formulário com dados do cliente
- POST: Atualiza dados do cliente
- Template: `cliente_form.html`

### pet_create_view(request, cliente_id)
- Método: GET/POST
- GET: Exibe formulário para novo pet
- POST: Cria novo pet e redireciona para detalhes do cliente
- Template: `pet_form.html`

### pet_edit_view(request, pet_id)
- Método: GET/POST
- GET: Exibe formulário com dados do pet
- POST: Atualiza dados do pet
- Template: `pet_form.html`

### pet_delete_view(request, pet_id)
- Método: POST
- Deleta o pet e redireciona para detalhes do cliente

## Campos de Formulário

### Formulário de Cliente
- Nome Completo (required)
- Telefone / WhatsApp (required)
- CPF (opcional)
- Rua (opcional)
- Número (opcional)
- Bairro (opcional)

### Formulário de Pet
- Nome do Pet (required)
- Raça (required)
- Porte (required): Pequeno, Médio, Grande
- Idade (opcional)

## Funcionalidades de Segurança

- Validação de formulários no servidor
- CSRF token em todos os formulários
- Proteção contra SQL Injection via ORM Django
- Mensagens de feedback ao usuário

## Integração com Admin

Ambos os modelos estão registrados no admin Django:

```
/admin/core/cliente/     - Gerenciar clientes
/admin/core/pet/         - Gerenciar pets
```

## Migrações

As migrações foram criadas e aplicadas:

```
core/migrations/0002_cliente_alter_pet_options_pet_atualizado_em_and_more.py
```

Para rodar novamente:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Exemplo de Dados

### Inserir dados via shell Django:

```python
from core.models import Cliente, Pet

# Criar cliente
cliente = Cliente.objects.create(
    nome_cliente='João da Silva',
    telefone='(11) 98888-7777',
    cpf='123.456.789-00',
    rua='Avenida Paulista',
    numero='1000',
    bairro='Bela Vista'
)

# Criar pet
pet = Pet.objects.create(
    cliente=cliente,
    nome_pet='Thor',
    raca_pet='Golden Retriever',
    porte_pet='grande',
    idade_pet='3 anos'
)
```

## Próximas Funcionalidades Sugeridas

1. Upload de foto para cliente/pet
2. Histórico de atendimentos por cliente
3. Agendamento integrado com cliente/pet
4. Exportar dados em PDF/Excel
5. Busca/Filtro de clientes
6. Sistema de permissões por usuário
7. API REST para integração mobile
