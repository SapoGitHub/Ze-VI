import json                                                         #Biblioteca para lidar com o JSON
import gspread                                                      #Biblioteca para lidar com planilhas
from oauth2client.service_account import ServiceAccountCredentials  #Biblioteca para gerar credenciais do tipo OAuth utilizadas pelo google
import datetime                                                     #Biblioteca com funções relacionadas ao tempo

#Função para conectar à planilha
def conecta_planilha(login):
    #Precisamos usar o scope ao adquirir um token de acesso
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    #Obtemos as credenciais
    credenciais = ServiceAccountCredentials.from_json_keyfile_dict(login, scope)

    google = gspread.authorize(credenciais)     #Conectamos
    print("Conectado ao Google.")

    return google.open("Bolão OWL").sheet1      #Abrimos a pagina 1 do arquivo

#Descrição do comando da aposta:
def owl_aposta(context,login,time1,placar1,x,placar2,time2,*data):
    #context    - Informações sobre a mensagem que foi enviada.
    #time1      - Nome de algum time
    #placar1    - Placar correspondente a este time
    #x          - Versus
    #time2      - Nome do outro time
    #placar2    - Placar correspondente a este outro time
    #*data      - Data da aposta (opcional)

    planilha = conecta_planilha(login)      #Se conecta com a planilha
    
    apostador=str(context.message.author) #Para sabermos quem esta apostando

    #Dicionários que vamos utilizar
    dsem = {"1":"SEG","2":"TER","3":"QUA","4":"QUI","5":"SEX","6":"SAB","7":"DOM"} #Dias da semana
    times = {   #Sinônimos para os nomes dos times
        "Shanghai Dragons":("shanghai","dragons","xangai dragons","shangai"),
        "Los Angeles Gladiators":("gladiators"),
        "San Francisco Shock":("schock","sf"),
        "Los Angeles Valiants":("valiants"),
        "Dallas Fuel":("dallas","fuel"),
        "Seoul Dynasty":("seoul","seul","dynasty"),
        "Boston Uprising":("boston","uprising"),
        "New York Excelsior":("ny","excelsior"),
        "London Spitfire":("london","spitfire"),
        "Philadelphia Fusion":("philadelphia","fusion")}
    nos={"ZéRomildo#1325":5,"Fitz#0746":6,"Sapo#0431":7}    #Nossa localização na tabela

    if (len(data)==0):  #Se não passamos nenhuma data, é no dia de hoje a aposta
        dia = dsem[datetime.date.today().strftime("%w")]+ " - " + datetime.date.today().strftime("%d") +"/"+datetime.date.today().strftime("%m")
    else:               #Se não, usamos a data informada
        dados=data[0].split("/")       #Vamos dividir entre dia e mês
        data_form=datetime.date(2018, int(dados[1]), int(dados[0]))  #Construir uma data a partir disto
        dia = dsem[data_form.strftime("%w")]+ " - " + data_form.strftime("%d") +"/"+data_form.strftime("%m") #E salvar

    timeshj=["",""]     #Onde vamos guardar os dois times que foram passados
    #Precisamos pegar o nome correto do primeiro time
    for tm in times:
        if time1.lower() in times[tm]:
            timeshj[0]=tm
            break

    #Precisamos pegar o nome correto do segundo time
    for tm in times:
        if time2.lower() in times[tm]:
            timeshj[1]=tm
            break

    #Buscamos todos os jogos do dia
    jogos = planilha.findall(dia)
    c=1             #Vamos adicionar um contador caso tenha mais de um jogo
    #Então podemos percorrer cada um dos elementos:
    for jogo in jogos:
        #E checar se o jogo desse dia é o que nos interessa:
        if ((planilha.cell(jogo.row, jogo.col+1).value == timeshj[0] or planilha.cell(jogo.row, jogo.col+1).value == timeshj[1])
            and
            (planilha.cell(jogo.row, jogo.col+3).value == timeshj[0] or planilha.cell(jogo.row, jogo.col+3).value == timeshj[1])):
            if (len(data)<=1):  #Se não informamos o dia, ou informamos somente o dia, é um dia de um único jogo
                linha=jogo.row  #Retornamos a linha
                break           #E saimos
            else:               #Se não temos um dia de jogos repetidos
                if (int(data[1])==c):#Se queremos do jogo em questão:
                    linha=jogo.row  #Retornamos a linha
                    break           #E saimos
                else:
                    c=c+1           #Se não, vamos procurar o proximo jogo

    #Com a linha vamos montar nossa aposta, primeiro precisamos saber a ordem
    if (planilha.cell(linha, 2).value==timeshj[0]):
        aposta=placar1+' x '+placar2
    else:
        aposta=placar2+' x '+placar1

    #Agora precisamos salvar a aposta, dependendo de quem apostou
    planilha.update_cell(linha, nos[apostador], aposta)

    #Vamos adicionar uma mensagem de apoio ao time vencedor.
    fala= "Aposta feita! Vai "   #Começo da fala
    if (int(placar1)>int(placar2)):
        fala=fala+timeshj[0]+"!"
    else:
        fala=fala+timeshj[1]+"!"
    return (fala)

#Comando para ver os jogos no dia
def owl_jogos(login,*data):
    #*data      - Data em que queremos ver os jogos
    planilha = conecta_planilha(login)      #Se conecta com a planilha
    
    dsem = {"1":"SEG","2":"TER","3":"QUA","4":"QUI","5":"SEX","6":"SAB","7":"DOM"} #Dias da semana

    if (len(data)==0):  #Se não passamos nenhuma data, é do dia de hoje que queremos ver os jogos
        dia = dsem[datetime.date.today().strftime("%w")]+ " - " + datetime.date.today().strftime("%d") +"/"+datetime.date.today().strftime("%m")
    else:               #Se não, usamos a data informada
        dados=data[0].split("/")       
        data=datetime.date(2018, int(dados[1]), int(dados[0]))  
        dia = dsem[data.strftime("%w")]+ " - " + data.strftime("%d") +"/"+data.strftime("%m") 

    #Buscamos todos os jogos do dia em questão
    jogos = planilha.findall(dia)

    #Então podemos percorrer cada um dos elementos e imprimir os jogos:
    partidas=""            #Onde vamos guardar os jogos
    for jogo in jogos:
             partidas=partidas+ planilha.cell(jogo.row, jogo.col+1).value+' x '+planilha.cell(jogo.row, jogo.col+3).value+"\n"
    return (partidas)


print ("Módulo do OWL importado.")
