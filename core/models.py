from django.db import models

class Pet(models.Model):
    nome_pet = models.CharField(max_length=100)
    raca_pet = models.CharField(max_length=100)
    porte_pet = models.CharField(max_length=20, choices=[
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
    ])
    # Add other fields as needed, like tutor foreign key, but for now, just these

    def __str__(self):
        return self.nome_pet
