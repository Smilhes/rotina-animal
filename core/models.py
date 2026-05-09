from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nome_cliente = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    rua = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_cliente

    class Meta:
        ordering = ['nome_cliente']


class Pet(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pets')
    nome_pet = models.CharField(max_length=100)
    raca_pet = models.CharField(max_length=100)
    porte_pet = models.CharField(max_length=20, choices=[
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
    ])
    idade_pet = models.CharField(max_length=20, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_pet

    class Meta:
        ordering = ['nome_pet']


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    hora_inicio = models.TimeField()
    tipo_servico = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_realizacao = models.DateField(null=True, blank=True)
    hora_realizacao = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    pago = models.BooleanField(default=False)
    recorrente = models.BooleanField(default=False)
    observacoes = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pet.nome_pet} - {self.cliente.nome_cliente} - {self.data}"

    class Meta:
        ordering = ['data', 'hora_inicio']

    @property
    def status_class(self):
        return {
            'pendente': 'secondary',
            'em_andamento': 'warning',
            'concluido': 'success',
            'cancelado': 'danger'
        }.get(self.status, 'secondary')
