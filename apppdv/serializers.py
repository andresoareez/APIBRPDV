from abc import ABC
from rest_framework import serializers
from .models import Estados, PontodeVenda, Rede, Bandeira, Regional, PDOHresults


class EstadosSerializer(serializers.Serializer, ABC):
    class Meta:
        model = Estados
        fields = '__all__'


class PdvSerializer(serializers.Serializer, ABC):
    class Meta:
        model = PontodeVenda
        fields = ['PDV', 'bandeira', 'canal', 'macroRegional', 'regional', 'cidade', 'estado', 'logradouro', 'numero',
                  'bairro', 'CEP']


class RedeSerializer(serializers.Serializer, ABC):
    class Meta:
        model = Rede
        fields = '__all__'


class BandeiraSerializer(serializers.Serializer, ABC):
    class Meta:
        model = Bandeira
        fields = '__all__'


class RegionalSerializer(serializers.Serializer, ABC):
    class Meta:
        model = Regional
        fields = '__all__'


class PdohSerializer(serializers.Serializer, ABC):
    class Meta:
        model = PDOHresults
        fiels = '__all__'
