from django.shortcuts import render
from rest_framework import viewsets,  generics, filters
from models import *
from serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend


class PDVInternView(viewsets.ModelViewSet):
    queryset = PontodeVenda.objects.all()
    serializer_class = PdvSerializer
    filter_backends = [DjangoFilterBackend, filter.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['estado']
    search_fields = ['pdv', 'bandeira', 'rede', 'canal', 'regional']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]


class PDVUserView(generics.ListAPIView):
    queryset = PontodeVenda.objects.all()
    serializer_class = PdvSerializer
    filter_backends = [DjangoFilterBackend, filter.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['estado']
    search_fields = ['pdv', 'bandeira', 'rede', 'canal', 'regional']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class PdohView(generics.ListAPIView):
    queryset = PDOHresults.objects.all()
    serializer_class = PdohSerializer
    filter_backends = [DjangoFilterBackend, filter.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['colaborador']
    search_fields = ['colaborador']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]




