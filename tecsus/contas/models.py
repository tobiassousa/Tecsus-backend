from django.db import models

class DadosBase(models.Model):
    TIPO_DOCUMENTO_CHOICES = (
        ('fatura', 'Fatura'),
        ('contrato', 'Contrato'),
    )

    dados = models.JSONField()
    data_envio = models.DateTimeField(auto_now_add=True)
    documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES)
    
    class Meta:
        abstract = True

class Agua(DadosBase):
    def __str__(self):
        return f'Dados Agua #{self.id} - Enviado em {self.data_envio}'

class Energia(DadosBase):
    def __str__(self):
        return f'Dados Energia #{self.id} - Enviado em {self.data_envio}'

class Gas(DadosBase):
    def __str__(self):
        return f'Dados Gas #{self.id} - Enviado em {self.data_envio}'
