# Generated by Django 3.2.25 on 2024-05-04 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertaagua',
            name='alert_consumo_atual',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='alertaagua',
            name='alert_consumo_media',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='alertaagua',
            name='alert_user_email',
            field=models.EmailField(max_length=1000),
        ),
    ]
