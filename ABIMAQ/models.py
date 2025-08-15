from django.db import models

class PesquisaABIMAQ(models.Model):
     STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('carregando', 'Carregando'),
        ('sucesso', 'Sucesso'),
        ('erro', 'Erro'), 
    )
     
     arquivo_upload = models.FileField(upload_to='uploads/')
     status = models.CharField(choices=STATUS_CHOICES,default='pendente')
     caminho_resultado = models.CharField(max_length=250,null=True, blank=True)
     data_criacao = models.DateTimeField(auto_now_add=True)


     def __str__(self):
        return f'Pesquisa #{self.id} - {self.status}'
     
     