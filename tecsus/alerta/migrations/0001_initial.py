# Generated by Django 5.0.3 on 2024-05-05 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlertaAgua',
            fields=[
                ('id_alerta', models.AutoField(primary_key=True, serialize=False)),
                ('id_user_alerta', models.CharField(max_length=10000)),
                ('alert_user_email', models.EmailField(max_length=1000)),
                ('alert_consumo_media', models.CharField(max_length=1000)),
                ('alert_consumo_atual', models.CharField(max_length=1000)),
                ('alert_conta', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='AlertaEnergia',
            fields=[
                ('id_alerta', models.AutoField(primary_key=True, serialize=False)),
                ('id_user_alerta', models.CharField(max_length=10000)),
                ('alert_user_email', models.EmailField(max_length=1000)),
                ('alert_consumo_media', models.CharField(max_length=1000)),
                ('alert_consumo_atual', models.CharField(max_length=1000)),
                ('alert_conta', models.CharField(max_length=10000)),
            ],
        ),
    ]