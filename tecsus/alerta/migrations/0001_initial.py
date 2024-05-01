
from django.db import migrations, models

class Migration(migrations.Migration):
    
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlertaAgua',
            fields=[
                ('id_alerta', models.AutoField(primary_key=True)),
                ('id_user_alerta', models.CharField(max_length=10000)),
                ('alert_user_email', models.CharField(max_length=10000)),
                ('alert_consumo_media', models.CharField(max_length=10000)),
                ('alert_consumo_atual', models.CharField(max_length=10000)),
                ('alert_conta', models.CharField(max_length=10000)),               
            ]
        )
    ]