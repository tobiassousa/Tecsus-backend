# Generated by Django 5.0.6 on 2024-05-20 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('energia', '0013_alter_fatocontratoenergia_num_contrato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fatocontratoenergia',
            name='num_instalacao',
            field=models.CharField(max_length=255, null=True),
        ),
    ]