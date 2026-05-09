from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_agendamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='data_realizacao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='agendamento',
            name='hora_realizacao',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
