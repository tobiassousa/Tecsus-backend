# Generated by Django 5.0.3 on 2024-05-12 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agua', '0004_remove_clientecontrato_id_cliente_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientecontrato',
            name='numero_cliente',
            field=models.IntegerField(null=True),
        ),
    ]