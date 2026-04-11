from django.db import models
from django.utils import timezone

# Tabelas auxiliares 
class StatusAgendamento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Status de agendamento"
        verbose_name_plural = "Status de agendamentos"


class TipoAtendimento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de atendimento"
        verbose_name_plural = "Tipos de atendimento"


class Porte(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20, unique=True)
    peso_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    peso_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nome


class Especie(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Espécie"
        verbose_name_plural = "Espécies"


class StatusLogistica(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Status de logística"
        verbose_name_plural = "Status de logística"



# Raça, Endereço, Cliente
class Raca(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    porte_referencia = models.ForeignKey(
        Porte,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Porte típico desta raça. O porte efetivo do pet é calculado pelo peso."
    )

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    id = models.AutoField(primary_key=True)
    logradouro = models.CharField(max_length=150)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    referencia = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.logradouro}, {self.numero}"


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome


# Pet
class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raca = models.ForeignKey(Raca, on_delete=models.SET_NULL, null=True, blank=True)
    data_nascimento = models.DateField(
        null=True,
        blank=True,
        help_text="Usado para calcular a idade atual do pet."
    )
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    observacoes_gerais = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    @property
    def idade_anos(self):
        """Calcula a idade do pet em anos a partir da data de nascimento."""
        if not self.data_nascimento:
            return None
        hoje = timezone.now().date()
        anos = hoje.year - self.data_nascimento.year
        # Ajuste caso o aniversário ainda não tenha ocorrido este ano
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            anos -= 1
        return anos

    def get_porte(self):
        """
        Retorna o porte do pet com base no peso atual,
        consultando a tabela Porte.
        """
        return Porte.objects.filter(
            peso_min__lte=self.peso,
            peso_max__gte=self.peso
        ).first()


class PetSaude(models.Model):
    GRAVIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    descricao = models.TextField()
    gravidade = models.CharField(max_length=20, choices=GRAVIDADE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Saúde do pet"
        verbose_name_plural = "Saúde dos pets"



# Serviços
class Servico(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"


class ServicoPorte(models.Model):
    id = models.AutoField(primary_key=True)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    porte = models.ForeignKey(Porte, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    duracao_estimada = models.IntegerField(help_text="Duração em minutos")

    class Meta:
        unique_together = ('servico', 'porte')
        verbose_name = "Preço por porte"
        verbose_name_plural = "Preços por porte"


# Agendamento
class Agendamento(models.Model):
    id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusAgendamento, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    possui_logistica = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Agendamento #{self.pk} — {self.pet.nome} em {self.data_hora:%d/%m/%Y %H:%M}"

    @property
    def cliente(self):
        """Atalho para acessar o cliente dono do pet."""
        return self.pet.cliente


class LogisticaAgendamento(models.Model):
    id = models.AutoField(primary_key=True)
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE)
    tipo_atendimento = models.ForeignKey(TipoAtendimento, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)
    horario_busca = models.DateTimeField(null=True, blank=True)
    horario_entrega = models.DateTimeField(null=True, blank=True)
    status_logistica = models.ForeignKey(
        StatusLogistica,
        on_delete=models.CASCADE
    )
    custo_transporte = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Logística de agendamento"
        verbose_name_plural = "Logísticas de agendamentos"


class AgendamentoServico(models.Model):
    id = models.AutoField(primary_key=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    preco_aplicado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('agendamento', 'servico')
        verbose_name = "Serviço do agendamento"
        verbose_name_plural = "Serviços do agendamento"


# Lembretes
class Lembrete(models.Model):
    TIPO_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'E-mail'),
        ('sms', 'SMS'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('enviado', 'Enviado'),
        ('falhou', 'Falhou'),
    ]

    id = models.AutoField(primary_key=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    data_envio = models.DateTimeField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    mensagem = models.TextField()


# Histórico
class HistoricoAtendimento(models.Model):
    id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de atendimento"
        verbose_name_plural = "Histórico de atendimentos"
        ordering = ['-data']
