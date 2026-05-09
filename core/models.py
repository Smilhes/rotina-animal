from django.db import models

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
