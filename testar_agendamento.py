#!/usr/bin/env python
import os
import django
from datetime import date, time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from core.models import Cliente, Pet, Agendamento

def testar_criacao_agendamento():
    # Pegar primeiro cliente e pet
    cliente = Cliente.objects.first()
    pet = Pet.objects.filter(cliente=cliente).first()

    print(f"Cliente encontrado: {cliente}")
    print(f"Pet encontrado: {pet}")

    if cliente and pet:
        # Criar agendamento
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            pet=pet,
            data=date.today(),
            hora_inicio=time(10, 0),
            tipo_servico='Banho e Tosa',
            valor=50.00
        )
        print(f'Agendamento criado: {agendamento}')
        print(f'Total de agendamentos: {Agendamento.objects.count()}')
        return True
    else:
        print('Cliente ou pet não encontrado')
        return False

if __name__ == "__main__":
    testar_criacao_agendamento()