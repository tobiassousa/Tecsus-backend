# Generated by Django 5.0.6 on 2024-05-19 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energia', '0010_enderecoenergia_delete_enderecoagua_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientecontrato',
            name='num_cliente',
            field=models.CharField(max_length=255, null=True),
        ),
    ]