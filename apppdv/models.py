from django.db import models
from django.contrib.auth.models import User


class Estados(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nome


class Regional(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Rede(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome


class Bandeira(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class PontodeVenda(models.Model):
    Regional = [
        ('Nordeste','NE')
        ('Norte', 'NO')
        ('Centro-Oeste', 'CEO')
        ('Sudeste', 'SUD')
        ('Sul', 'SU')
    ]

    # Estados = [
    #     ('AC', 'Acre')
    #     ('AL', 'Alagoas')
    #     ('AM', 'Amapá')
    #     ('BA', 'Bahia')
    #     ('CE', 'Ceará')
    #     ('DF', 'Distrito Federal')
    #     ('ES', 'Espirito Santo')
    #     ('GO', 'Goiás')
    #     ('MA', 'Maranhão')
    #     ('MT', 'Mato Grosso')
    #     ('MS', 'Mato Grosso do Sul')
    #     ('MG', 'Minas Gerais')
    #     ('PA', 'Pará')
    #     ('PB', 'Paraíba')
    #     ('PE', 'Pernambuco')
    #     ('PI', 'Piauí')
    #     ('RJ', 'Rio de Janeiro')
    #     ('RN', 'Rio Grande do Norte')
    #     ('RS', 'Rio Grande do Sul')
    #     ('RO', 'Rondônia')
    #     ('RO', 'Roraima')
    #     ('SC', 'Santa Catarina')
    #     ('SP', 'São Paulo')
    #     ('SE', 'Sergipe')
    #     ('TO', 'Tocantins')
    # ]
    CANALPDV = [
        ('Atacado', 'Atacado')
        ('Varejo', 'Varejo')

    ]

    id = models.AutoField(primary_key=True)
    PDV = models.CharField(max_length=200, unique=True, verbose_name='Ponto de Venda')
    bandeira = models.ForeignKey(Bandeira, to_field='nome', on_delete=models.CASCADE)
    canal = models.CharField(max_length=10, choices=CANALPDV, verbose_name='Canal do PDV')
    macroRegional = models.CharField(max_length=50, to_field=Regional, verbose_name='Macroregional')
    regional = models.ForeignKey(Regional, to_field='name', verbose_name='Regional', on_delete=models.CASCADE)
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.ForeignKey(Estados, to_field='sigla', on_delete=models.CASCADE, verbose_name='Estado')
    logradouro = models.CharField(max_length=255, verbose_name='logradouro')
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50, verbose_name='Bairro')
    CEP = models.CharField(max_length=9)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Ponto de Venda'
        verbose_name_plural = 'Pontos de Venda'

    def __str__(self):
        return self.PDV


class CostPassagens(models.Model):
    id = models.AutoField(primary_key=True)
    cidade = models.ForeignKey(PontodeVenda, to_field='cidade', on_delete=models.CASCADE, db_index=True)
    valeA = models.FloatField(max_length=3, blank=True, null=True)
    valeB = models.FloatField(max_length=3, blank=True, null=True)
    valeC = models.FloatField(max_length=3, blank=True, null=True)
    valeD = models.FloatField(max_length=3, blank=True, null=True)
    valeE = models.FloatField(max_length=3, blank=True, null=True)
    valeF = models.FloatField(max_length=3, blank=True, null=True)
    valeG = models.FloatField(max_length=3, blank=True, null=True)
    imA = models.FloatField(max_length=5, blank=True, null=True, verbose_name='InterMunicipal 10 km')
    imB = models.FloatField(max_length=5, blank=True, null=True, verbose_name='InterMunicipal 30 km')
    imC = models.FloatField(max_length=5, blank=True, null=True, verbose_name='InterMunicipal 50 km')
    imD = models.FloatField(max_length=5, blank=True, null=True, verbose_name='InterMunicipal 70 km')
    imE = models.FloatField(max_length=5, blank=True, null=True, verbose_name='InterMunicipal 90 km')

    def __str__(self):
        return self.cidade


class PDOHresults(models.Model):
    id = models.AutoField(primary_key=True)
    colaborador = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='Promotores')
    produtividade = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Produtividade')
    deslocamento = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Deslocamento')
    ocio = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Ócio')
    hrsnaocontab = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Horas não contabilizadas')

    def __str__(self):
        return self.colaborador


