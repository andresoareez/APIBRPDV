import pandas as pd
from datetime import time
from datetime import datetime
import xlwt

tarefas = pd.read_excel('tarefas.xls')
visitas = pd.read_excel('check.xls')
dicionarios = pd.read_excel('dicionario.xls')
perfil = pd.read_excel('colaboradores.xls')

# Ajustando a planilha com Perfil de Acesso do Colaborador
perfil.columns
PerfilDeAcesso = perfil[['Nome do Colaborador', 'Perfil de acesso']]
PerfilDeAcesso = PerfilDeAcesso.rename(columns={'Nome do Colaborador':'Colaborador'})

#Função de Conversão para Horas, Minutos e Segundos

def td_to_hmsstr(td):
    """
    convert a timedelta object td to a string in HH:MM:SS format.
    """
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'


#Selecionando só checkin manual
manual = visitas.loc[visitas['Tipo de Checkin'] == 'Checkin Manual']

#Removendo linhas faltantes
nonull = manual.dropna(subset=['Hora Saída'], axis=0)

#Ordenando corretamente os index
nonull.index = range(nonull.shape[0])

#Criando novas colunas de Data e Hora
deslocamento = nonull
deslocamento['Data'] = [d.date() for d in deslocamento['Hora Entrada']]
deslocamento['Hora'] = [d.time() for d in deslocamento['Hora Entrada']]

#Transformando valores da coluna em formado data & hora
deslocamento['Data'] = pd.to_datetime(deslocamento['Data'])
deslocamento['Hora'] = pd.to_datetime(deslocamento['Hora'], format='%H:%M:%S')

#Criando coluna com informação "Deslocamento"
deslocamento['Tipo'] = 'Deslocamento'

#Selecionando as colunas que desejo trabalhar
checkin = deslocamento[['Colaborador', 'Colaborador Superior', 'Estado', 'Ponto de Venda', 'Fora do roteiro','Tipo', 'Data', 'Hora',]]

#Renomeando coluna Fora do roteiro
checkin = checkin.rename({'Fora do roteiro' : 'Cliente'}, axis=1)

ocio = nonull
#Criando novas colunas de Data e Hora
ocio['Data'] = [d.date() for d in ocio['Hora Saída']]
ocio['Hora'] = [d.time() for d in ocio['Hora Saída']]

#Transformando valores da coluna em formado data & hora
ocio['Data'] = pd.to_datetime(ocio['Data'])
ocio['Hora'] = pd.to_datetime(ocio['Hora'], format='%H:%M:%S')

ocio['Tipo'] = 'Ocio'

#Selecionando as colunas que desejo trabalhar

checkout = ocio[['Colaborador', 'Colaborador Superior', 'Estado', 'Ponto de Venda', 'Fora do roteiro','Tipo', 'Data', 'Hora',]]

#Renomeando coluna Fora do roteiro
checkout = checkout.rename({'Fora do roteiro' : 'Cliente'}, axis=1)

tarefas['Data'] = [d.date() for d in tarefas['Data de Conclusão']]
tarefas['Hora'] = [d.time() for d in tarefas['Data de Conclusão']]

tarefas['Data'] = pd.to_datetime(tarefas['Data'])
tarefas['Hora'] = pd.to_datetime(tarefas['Hora'], format = '%H:%M:%S')

tarefas['Tipo'] = 'Produtividade'

produtividadeSemDicionario = tarefas[['Responsável', 'Colaborador Superior', 'Estado', 'Ponto de Venda', 'Rótulo','Tipo', 'Data', 'Hora']]
dicionario = pd.merge(produtividadeSemDicionario, dicionarios, on=['Rótulo'], how="left")

produtividade = dicionario.rename({'Responsável':'Colaborador', 'Rótulo':'Cliente'}, axis=1)

#Concatenando
PDOH = pd.concat([checkin, checkout, produtividade])

#Selecionando Filtros
PDOH.sort_values(by=['Colaborador', 'Data', 'Hora'], inplace = True)

#Reorganizando índices
PDOH.index = range(PDOH.shape[0])


#Criando Variável para receber os valores
timein = []
linhas = PDOH.shape[0] - 1

#Criando uma das condições e armazenando em uma variável
t0 = PDOH['Hora'][1] - PDOH['Hora'][1]

#Criando um laço de repetição por linha

for i in range(linhas):
    if PDOH['Data'][i+1] != PDOH['Data'][i]:
        timein.append(t0)
    else:
        timein.append(PDOH['Hora'][i+1] - PDOH['Hora'][i])

#Criando Data Frame com a variável que armazenou as informações
timein= pd.DataFrame(timein)

#Adicionando uma coluna Nula na primeira linha da coluna
timein.loc[-1] = t0
timein.index = timein.index + 1
timein = timein.sort_index()

# Conferindo se a coluna de cálculos criada é do mesmo tamanho da do PDOH
timein.shape[0] - PDOH.shape[0]

#Adicionando coluna de cálculos ao PDOH
PDOH['Tempo Investido'] = timein

info = pd.read_excel("colaboradores.xls")

colaboradores = info[["Nome do Colaborador", "Perfil de acesso"]]
colaboradores = colaboradores.rename(columns = {"Nome do Colaborador": "Colaborador"})
final = pd.merge(PDOH, colaboradores, on=['Colaborador'], how="left")

desl = final['Tipo'] == 'Deslocamento'
deslocamento = final[desl]
DeslocamentoColaboradores = deslocamento.groupby(['Colaborador'])
SomaDeslocamentoPorColaborador = DeslocamentoColaboradores['Tempo Investido'].sum()
SomaDeslocamentoPorColaborador = pd.DataFrame(SomaDeslocamentoPorColaborador)
SomaDeslocamentoPorColaborador = SomaDeslocamentoPorColaborador.reset_index()
SomaDeslocamentoPorColaborador['H:M:S'] = SomaDeslocamentoPorColaborador['Tempo Investido'].apply(td_to_hmsstr)
SomaDeslocamentoPorColaborador = SomaDeslocamentoPorColaborador.rename(columns={'H:M:S':'Deslocamento'})

Oc = final['Tipo'] == 'Ocio'
Ocio = final[Oc]
OcioColaboradores = Ocio.groupby(['Colaborador'])
SomaOcioPorColaborador = OcioColaboradores['Tempo Investido'].sum()
SomaOcioPorColaborador = pd.DataFrame(SomaOcioPorColaborador)
SomaOcioPorColaborador['H:M:S'] = SomaOcioPorColaborador['Tempo Investido'].apply(td_to_hmsstr)
SomaOcioPorColaborador = SomaOcioPorColaborador.reset_index()
SomaOcioPorColaborador = SomaOcioPorColaborador.rename(columns={'H:M:S':'Ocio'})

Prod = final['Tipo'] == 'Produtividade'
Produtividade = final[Prod]
ProdutividadeColaboradores = Produtividade.groupby(['Colaborador'])
SomaProdutividadePorColaborador = ProdutividadeColaboradores['Tempo Investido'].sum()
SomaProdutividadePorColaborador = pd.DataFrame(SomaProdutividadePorColaborador)
SomaProdutividadePorColaborador['H:M:S'] = SomaProdutividadePorColaborador['Tempo Investido'].apply(td_to_hmsstr)
SomaProdutividadePorColaborador = SomaProdutividadePorColaborador.reset_index()
SomaProdutividadePorColaborador = SomaProdutividadePorColaborador.rename(columns={'H:M:S':'Produtividade'})

tipos = PDOH.groupby(['Colaborador'])
HorasTotaisRegistradas = tipos['Tempo Investido'].sum()
HorasTotaisRegistradas = pd.DataFrame(HorasTotaisRegistradas)
HorasTotaisRegistradas = HorasTotaisRegistradas.reset_index()
JornadaDeTrabalho = pd.merge(HorasTotaisRegistradas, PerfilDeAcesso, on=['Colaborador'], how='left')


### Criacao da jornada
InicioDaJornadaDia = '18/01/2018 08:00'
InicioDoIntervaloDoAlmoco = '18/01/2018 12:00'
FimDoIntervaloDoAlmoco = '18/01/2018 14:00'
FimDaJornadaDia='18/01/2018 18:00'
FimDaJornadaSábado = '23/01/2018 12:00'
HoraEntrada = datetime.strptime(InicioDaJornadaDia, '%d/%m/%Y %H:%M')
HoraAlmoco = datetime.strptime(InicioDoIntervaloDoAlmoco, '%d/%m/%Y %H:%M')
HoraEntrada2 = datetime.strptime(FimDoIntervaloDoAlmoco, '%d/%m/%Y %H:%M')
HoraSaida = datetime.strptime(FimDaJornadaDia, '%d/%m/%Y %H:%M')
HoraSaidaSabado = datetime.strptime(FimDaJornadaSábado, '%d/%m/%Y %H:%M')

manha = HoraAlmoco - HoraEntrada
tarde = HoraSaida - HoraEntrada2
turnodianormal = (manha + tarde) *5
turnoCLT = turnodianormal + manha

HorasCorrigidas = []
linha = JornadaDeTrabalho.shape[0]


for i in range(linha):
    if JornadaDeTrabalho['Tempo Investido'][i] > turnoCLT:
        HorasCorrigidas.append(turnoCLT)
    else:
        HorasCorrigidas.append(JornadaDeTrabalho['Tempo Investido'][i])

HorasCorrigidas = pd.DataFrame(HorasCorrigidas)
JornadaDeTrabalho['Horas Corrigidas'] = HorasCorrigidas
JornadaDeTrabalho['Horas Não Contabilizadas'] = turnoCLT - JornadaDeTrabalho['Horas Corrigidas']
JornadaDeTrabalho['H:M:S'] = JornadaDeTrabalho['Horas Não Contabilizadas'].apply(td_to_hmsstr)
HorasNaoContabilizadas = JornadaDeTrabalho[['Colaborador', 'Tempo Investido', 'H:M:S']]
HorasNaoContabilizadas = HorasNaoContabilizadas.rename(columns={'H:M:S':'Horas Não Contabilizadas'})

P = SomaProdutividadePorColaborador[['Colaborador', 'Produtividade']]
D = SomaDeslocamentoPorColaborador[['Colaborador', 'Deslocamento']]
O = SomaOcioPorColaborador[['Colaborador', 'Ocio']]
H = HorasNaoContabilizadas[['Colaborador', 'Horas Não Contabilizadas']]


A = pd.merge(P, D, on=['Colaborador'], how="left")
B = pd.merge(O, H, on=['Colaborador'], how="left")
PDOHFINAL = pd.merge(A, B, on=['Colaborador'], how='left')

PDOHFINAL.head(10)
PDOHFINAL.to_excel('PDOH.xls')


