# Generated by Django 5.0.3 on 2024-05-05 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energia', '0002_remove_proenergia_contrato_energia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratoenergia',
            name='dem_fora_ponta',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='contratoenergia',
            name='dem_ponta',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='contratoenergia',
            name='hor_ponta',
            field=models.CharField(max_length=1000),
        ),
    ]
