from django.shortcuts import render, redirect
from .models import Pet

# Mock Data: Simulando banco de dados para o Dashboard
DASHBOARD_DATA = {
    'stats': {'hoje': 12, 'pendentes': 5, 'concluidos': 7},
    'agenda': [
        {'id': 1, 'horario': '09:00', 'pet': 'Thor', 'tutor': 'João Silva', 'servico': 'Banho e Tosa', 'status': 'Em andamento', 'status_class': 'warning'},
        {'id': 2, 'horario': '10:30', 'pet': 'Mel', 'tutor': 'Maria Souza', 'servico': 'Corte de Unha', 'status': 'Pendente', 'status_class': 'secondary'},
        {'id': 3, 'horario': '14:00', 'pet': 'Rex', 'tutor': 'Carlos Lima', 'servico': 'Banho G', 'status': 'Concluído', 'status_class': 'success'},
    ]
}

# Mock Data: Histórico
HISTORICO_DATA = [
    {'data': '10/05/2023', 'pet': 'Thor', 'tutor': 'João Silva', 'servico': 'Banho', 'valor': 'R$ 80,00'},
    {'data': '12/05/2023', 'pet': 'Luna', 'tutor': 'Ana Paula', 'servico': 'Tosa Higiênica', 'valor': 'R$ 60,00'},
]

def login_view(request):
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'dashboard.html', {'dados': DASHBOARD_DATA})

def cadastro_cliente_view(request):
    return render(request, 'cadastro_cliente.html')

def agendamento_view(request):
    return render(request, 'agendamento.html')

def historico_view(request):
    return render(request, 'historico.html', {'historico': HISTORICO_DATA})

def cadastro_pet_view(request):
    if request.method == 'POST':
        nome_pet = request.POST.get('nome_pet')
        raca_pet = request.POST.get('raca_pet')
        porte_pet = request.POST.get('porte_pet')
        # For now, just save the pet, ignoring tutor fields
        Pet.objects.create(nome_pet=nome_pet, raca_pet=raca_pet, porte_pet=porte_pet)
        return redirect('dashboard')  # or some success page
    return render(request, 'cadastro_pet.html')