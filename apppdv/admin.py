from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class PontodeVendaAdmin(ImportExportModelAdmin):
    list_display = [
        'PDV',
        'bandeira',
        'rede',
        'canal',
        'macroRegional',
        'regional',
        'cidade',
        'estado',
        ]
    list_display_links = [
        'PDV',
        'bandeira',
        'rede'
    ]
    list_filter = [
        'PDV',
        'bandeira',
        'rede',
        'canal',
        'cidade',
        'estado',
    ]
    search_fields = [
        'PDV',
        'bandeira',
        'rede',
    ]
    list_per_page = 50


class EstadosAdmin(ImportExportModelAdmin):
    list_display = [
        'sigla',
    ]
    list_filter = [
        'sigla',
    ]
    list_per_page = 50


class RegionalAdmin(ImportExportModelAdmin):
    list_display = [
        'nome',
    ]
    list_filter = [
        'nome',
    ]
    list_per_page = 50


class RedeAdmin(ImportExportModelAdmin):
    list_display = [
        'nome',
    ]
    list_filter = [
        'nome',
    ]
    list_per_page = 50


class BandeiraAdmin(ImportExportModelAdmin):
    list_display = [
        'nome',
    ]
    list_filter = [
        'nome',
    ]
    list_per_page = 50


class PassagensAdmin(ImportExportModelAdmin):
    list_display = [
        'cidade'
    ]
    list_filter = [
        'cidade'
    ]
    list_per_page = 50


admin.site.register(Bandeira, BandeiraAdmin)
admin.site.register(CostPassagens, PassagensAdmin)
admin.site.register(Rede, RedeAdmin)
admin.site.register(Regionais, RegionalAdmin)
admin.site.register(Estados, EstadosAdmin)
admin.site.register(PontodeVenda, PontodeVendaAdmin)





