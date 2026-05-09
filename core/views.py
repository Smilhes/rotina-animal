from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Cliente, Pet, Agendamento

# Mock Data: Simulando banco de dados para o Dashboard
DASHBOARD_DATA = {
    'stats': {'hoje': 12, 'pendentes': 5, 'concluidos': 7},
    'agenda': [
        {'id': 1, 'horario': '09:00', 'pet': 'Thor', 'tutor': 'João Silva', 'servico': 'Banho e Tosa', 'status': 'Em andamento', 'status_class': 'warning'},
        {'id': 2, 'horario': '10:30', 'pet': 'Mel', 'tutor': 'Maria Souza', 'servico': 'Corte de Unha', 'status': 'Pendente', 'status_class': 'secondary'},
        {'id': 3, 'horario': '14:00', 'pet': 'Rex', 'tutor': 'Carlos Lima', 'servico': 'Banho G', 'status': 'Concluído', 'status_class': 'success'},
    ]
}

HISTORICO_MOCK = [
    {'data': '15/10/2023', 'pet': 'Thor', 'raca': 'Golden', 'servico': 'Banho + Tosa', 'valor': '120,00', 'status': 'Pago'},
    {'data': '14/10/2023', 'pet': 'Mel', 'raca': 'Poodle', 'servico': 'Corte de Unha', 'valor': '30,00', 'status': 'Pago'},
    {'data': '10/10/2023', 'pet': 'Bolinha', 'raca': 'SRD', 'servico': 'Banho M', 'valor': '60,00', 'status': 'Pendente'},
]

def login_view(request):
    return render(request, 'login.html')

def dashboard_view(request):
    hoje = timezone.now().date()
    
    # Agendamentos de hoje (ativos no dashboard)
    agendamentos_hoje_visiveis = Agendamento.objects.filter(
        data=hoje
    ).filter(
        Q(status__in=['pendente', 'em_andamento']) |
        Q(status='concluido', pago=False)
    ).order_by('hora_inicio')

    hoje_agendamentos = Agendamento.objects.filter(
        data=hoje
    ).exclude(status='cancelado')
    
    # Estatísticas
    stats = {
        'hoje': hoje_agendamentos.count(),
        'pendentes': hoje_agendamentos.filter(status='pendente').count(),
        'concluidos': hoje_agendamentos.filter(status='concluido').count(),
    }
    
    # Agendamentos futuros (não hoje)
    agendamentos_futuros = Agendamento.objects.filter(
        data__gt=hoje
    ).filter(
        Q(status__in=['pendente', 'em_andamento']) |
        Q(status='concluido', pago=False)
    ).order_by('data', 'hora_inicio')
    
    context = {
        'stats': stats,
        'agendamentos_hoje': agendamentos_hoje_visiveis,
        'agendamentos_futuros': agendamentos_futuros,
        'hoje': hoje,
    }
    
    return render(request, 'dashboard.html', context)

def agendamento_view(request):
    if request.method == 'POST':
        # Processar o formulário de agendamento
        cliente_id = request.POST.get('cliente_id')
        pet_id = request.POST.get('pet_id')
        data = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        tipo_servico = request.POST.get('tipo_servico')
        valor = request.POST.get('valor')
        recorrente = request.POST.get('recorrente') == 'on'
        observacoes = request.POST.get('observacoes', '')

        # Validações básicas
        if not all([cliente_id, pet_id, data, hora_inicio, tipo_servico]):
            messages.error(request, 'Todos os campos obrigatórios devem ser preenchidos.')
            return redirect('agendamento')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            pet = Pet.objects.get(id=pet_id, cliente=cliente)

            # Criar agendamento
            agendamento = Agendamento.objects.create(
                cliente=cliente,
                pet=pet,
                data=data,
                hora_inicio=hora_inicio,
                tipo_servico=tipo_servico,
                valor=valor if valor else None,
                recorrente=recorrente,
                observacoes=observacoes
            )

            messages.success(request, f'Agendamento criado com sucesso para {pet.nome_pet} em {data} às {hora_inicio}!')
            return redirect('dashboard')

        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')
        except Pet.DoesNotExist:
            messages.error(request, 'Pet não encontrado ou não pertence ao cliente selecionado.')
        except Exception as e:
            messages.error(request, f'Erro ao criar agendamento: {str(e)}')

        return redirect('agendamento')

    return render(request, 'agendamento.html')

@require_http_methods(["GET"])
def api_buscar_clientes(request):
    """API para buscar clientes por nome ou CPF"""
    termo = request.GET.get('termo', '').strip()
    
    if not termo or len(termo) < 2:
        return JsonResponse({'clientes': []})
    
    # Busca por nome ou CPF
    clientes = Cliente.objects.filter(
        nome_cliente__icontains=termo
    ) | Cliente.objects.filter(
        cpf__icontains=termo
    )[:20]  # Limita a 20 resultados
    
    dados = {
        'clientes': [
            {
                'id': cliente.id,
                'nome': cliente.nome_cliente,
                'telefone': cliente.telefone,
                'cpf': cliente.cpf or 'N/A',
                'total_pets': cliente.pets.count()
            }
            for cliente in clientes
        ]
    }
    
    return JsonResponse(dados)

@require_http_methods(["GET"])
def api_buscar_pets(request, cliente_id):
    """API para obter pets de um cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    pets = cliente.pets.all()
    
    dados = {
        'cliente': {
            'id': cliente.id,
            'nome': cliente.nome_cliente,
            'telefone': cliente.telefone
        },
        'pets': [
            {
                'id': pet.id,
                'nome': f"{pet.nome_pet} ({pet.raca_pet})",
                'nome_simples': pet.nome_pet,
                'raca': pet.raca_pet,
                'porte': pet.get_porte_pet_display(),
                'idade': pet.idade_pet or 'N/A'
            }
            for pet in pets
        ]
    }
    
    return JsonResponse(dados)

def historico_view(request):
    status = request.GET.get('status', 'todos')
    query = request.GET.get('q', '').strip()

    historico_query = Agendamento.objects.filter(
        Q(status='cancelado') | Q(status='concluido', pago=True)
    )

    if status in ['concluido', 'cancelado']:
        historico_query = historico_query.filter(status=status)

    if query:
        historico_query = historico_query.filter(
            Q(pet__nome_pet__icontains=query) |
            Q(cliente__nome_cliente__icontains=query) |
            Q(tipo_servico__icontains=query)
        )

    historico = historico_query.order_by('-data', '-hora_inicio')
    return render(request, 'historico.html', {
        'historico': historico,
        'selected_status': status,
        'query': query,
    })

# --- CLIENTES E PETS ---

def cadastro_cliente_view(request):
    """Lista todos os clientes"""
    clientes = Cliente.objects.all()
    return render(request, 'cadastro_cliente.html', {'clientes': clientes})

def cliente_detail_view(request, cliente_id):
    """Mostra detalhes de um cliente e seus pets"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    pets = cliente.pets.all()
    return render(request, 'cliente_detail.html', {'cliente': cliente, 'pets': pets})

def cliente_create_view(request):
    """Cria novo cliente"""
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf', '')
        rua = request.POST.get('rua', '')
        numero = request.POST.get('numero', '')
        bairro = request.POST.get('bairro', '')
        
        cliente = Cliente.objects.create(
            nome_cliente=nome_cliente,
            telefone=telefone,
            cpf=cpf if cpf else None,
            rua=rua,
            numero=numero,
            bairro=bairro
        )
        messages.success(request, f'Cliente {nome_cliente} cadastrado com sucesso!')
        return redirect('cliente_detail', cliente_id=cliente.id)
    
    return render(request, 'cliente_form.html', {'modo': 'criar'})

def cliente_edit_view(request, cliente_id):
    """Edita um cliente existente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        cliente.nome_cliente = request.POST.get('nome_cliente')
        cliente.telefone = request.POST.get('telefone')
        cliente.cpf = request.POST.get('cpf', '') or None
        cliente.rua = request.POST.get('rua', '')
        cliente.numero = request.POST.get('numero', '')
        cliente.bairro = request.POST.get('bairro', '')
        cliente.save()
        messages.success(request, 'Cliente atualizado com sucesso!')
        return redirect('cliente_detail', cliente_id=cliente.id)
    
    return render(request, 'cliente_form.html', {'cliente': cliente, 'modo': 'editar'})

# --- PETS ---

def pet_create_view(request, cliente_id):
    """Cria novo pet para um cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        nome_pet = request.POST.get('nome_pet')
        raca_pet = request.POST.get('raca_pet')
        porte_pet = request.POST.get('porte_pet')
        idade_pet = request.POST.get('idade_pet', '')
        
        Pet.objects.create(
            cliente=cliente,
            nome_pet=nome_pet,
            raca_pet=raca_pet,
            porte_pet=porte_pet,
            idade_pet=idade_pet
        )
        messages.success(request, f'Pet {nome_pet} adicionado com sucesso!')
        return redirect('cliente_detail', cliente_id=cliente.id)
    
    return render(request, 'pet_form.html', {'cliente': cliente, 'modo': 'criar'})

def pet_edit_view(request, pet_id):
    """Edita um pet existente"""
    pet = get_object_or_404(Pet, id=pet_id)
    cliente_id = pet.cliente.id
    
    if request.method == 'POST':
        pet.nome_pet = request.POST.get('nome_pet')
        pet.raca_pet = request.POST.get('raca_pet')
        pet.porte_pet = request.POST.get('porte_pet')
        pet.idade_pet = request.POST.get('idade_pet', '')
        pet.save()
        messages.success(request, 'Pet atualizado com sucesso!')
        return redirect('cliente_detail', cliente_id=cliente_id)
    
    return render(request, 'pet_form.html', {'pet': pet, 'cliente': pet.cliente, 'modo': 'editar'})

def pet_delete_view(request, pet_id):
    """Deleta um pet"""
    pet = get_object_or_404(Pet, id=pet_id)
    cliente_id = pet.cliente.id
    
    if request.method == 'POST':
        nome_pet = pet.nome_pet
        pet.delete()
        messages.success(request, f'Pet {nome_pet} removido com sucesso!')
    
    return redirect('cliente_detail', cliente_id=cliente_id)

# --- APIs PARA DASHBOARD ---

@require_http_methods(["POST"])
def api_iniciar_agendamento(request, agendamento_id):
    """Inicia um agendamento (muda status para 'em_andamento')"""
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    
    if agendamento.status == 'pendente':
        agendamento.status = 'em_andamento'
        now = timezone.now()
        if not agendamento.data_realizacao:
            agendamento.data_realizacao = now.date()
        if not agendamento.hora_realizacao:
            agendamento.hora_realizacao = now.time()
        agendamento.save()
        return JsonResponse({'success': True, 'status': agendamento.status, 'status_class': agendamento.status_class})
    
    return JsonResponse({'success': False, 'message': 'Não é possível iniciar este agendamento'})

@require_http_methods(["POST"])
def api_concluir_agendamento(request, agendamento_id):
    """Conclui um agendamento (muda status para 'concluido')"""
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    
    if agendamento.status == 'em_andamento':
        agendamento.status = 'concluido'
        agendamento.save()
        return JsonResponse({'success': True, 'status': agendamento.status, 'status_class': agendamento.status_class})
    
    return JsonResponse({'success': False, 'message': 'Não é possível concluir este agendamento'})

@require_http_methods(["POST"])
def api_marcar_pago(request, agendamento_id):
    """Marca um agendamento como pago"""
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    
    agendamento.pago = True
    agendamento.save()
    
    return JsonResponse({'success': True, 'pago': agendamento.pago})

@require_http_methods(["POST"])
def api_cancelar_agendamento(request, agendamento_id):
    """Cancela um agendamento"""
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    
    if agendamento.status in ['pendente', 'em_andamento']:
        agendamento.status = 'cancelado'
        agendamento.save()
        return JsonResponse({'success': True, 'status': agendamento.status, 'status_class': agendamento.status_class})
    
    return JsonResponse({'success': False, 'message': 'Não é possível cancelar este agendamento'})