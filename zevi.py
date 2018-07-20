##ZÉ VI
##Desenvolvido por:     Jhordan Silveira de Borba
##E-mail:               jhordandecacapava@gmail.com
##Website:              https://sapogithub.github.io
##Mais informações:     https://github.com/SapoGitHub/Ze-VI/wiki
##2018

import random                                                       #Biblioteca para comandos aleatorios
import discord                                                      #Biblioteca para trabalhar com o discord
from discord.ext import commands                                    
import tweepy                                                       #Biblioteca para lidar com o Twitter
import json                                                         #Biblioteca para lidar com o JSON
import sys                                                          #Biblioteca que prove recursos relacionados ao interpretador
import os                                                           #Biblioteca para lidar com o Sistema Operacional
import gspread                                                      #Biblioteca para lidar com planilhas
from oauth2client.service_account import ServiceAccountCredentials  #Biblioteca para gerar credenciais do tipo OAuth utilizadas pelo google
import datetime                                                     #Biblioteca com funções relacionadas ao tempo
from repustate import Client                                        #Biblioteca para fazer análise de sentimento
from langdetect import detect                                       #Biblioteca para detectar língua sem limite

#DADOS SENSÍVEIS----------------------------------------------------------------------------------------------------------------
#Vamos montar nossa private key do google
var_amb=os.environ["private_key"]   #Recebemos a variável
dividido=var_amb.split("\\n")       #Dividimos onde tem \n
chave=""                            #Onde vamos remontar
for linha in dividido:
    if (len(linha)>0):              #Nossa última linha é apenas '' e queremos deixar assim
        chave=chave+linha+"\n"


token = os.environ['token']                                 #Discord: Token
consumer_key = os.environ['consumer_key']                   #Twitter: Consumer Key (API Key)
consumer_secret = os.environ['consumer_secret']             #Twitter: Consumer Secret (API Secret)
access_token = os.environ['access_token']                   #Twitter: Access Token
access_token_secret = os.environ['access_token_secret']     #Twitter: Access Token Secret
api_key=os.environ['api_key']                               #Repustate: API KEY
login = {                                                   #Google : Dados do API do Google
    "type": os.environ['type'],
    "private_key_id": os.environ['private_key_id'],
    "private_key": chave,
    "client_email": os.environ['client_email'],
    "client_id": os.environ['client_id']}

#CONFIGURAÇÃO DISCORD---------------------------------------------------------------------------------------------------------
bot = commands.Bot(command_prefix='!', description='Vamo esculachar!!!')

#Vamos printar quando conectar ao discord
@bot.event
async def on_ready():
    print('Conectado ao Discord.')
    #print(bot.user.name)

#CONEXÃO TWITTER-------------------------------------------------------------------------------------------------------------
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print("Conectado ao Twitter.")

#CONEXÃO PLANILHA DO GOOGLE--------------------------------------------------------------------------------------------------

def conecta_planilha():
    #Precisamos usar o scope ao adquirir um token de acesso
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    #Obtemos as credenciais
    credenciais = ServiceAccountCredentials.from_json_keyfile_dict(login, scope)

    google = gspread.authorize(credenciais)     #Conectamos
    print("Conectado ao Google.")

    return google.open("Bolão OWL").sheet1      #Abrimos a pagina 1 do arquivo

conecta_planilha()  #Vamos conectar uma vez pra testar
#CONEXÃO REPUSTATE----------------------------------------------------------------------------------------------------------
#client = Client(api_key=api_key, version='v4')
#print("Conectado ao Repustate.") 

#COMANDOS--------------------------------------------------------------------------------------------------------------------
#Comando da Bola 8
@bot.command(name='bola8',                                                                  #Como pode ser chamado a função no discord
                description="Faça uma pergunta que possa ser respondida com sim ou não.",   #Descrição que aparece no !help bola8
                brief="Respostas sim/não.",                                                 #Descrição que aparece no !help
                aliases=['bola_oito', 'bolaoito'],                                          #Outras formas de chamar a mesma função
                pass_context=True)                                                          #Se vai passar o contexto
async def ball(context):
    #context    - Informações sobre a mensagem que foi enviada.
    
    respostas=['sim','não']
    await bot.say(context.message.author.mention+': a resposta para sua pergunta é ... '+random.choice(respostas)+'!')

#Comando para twittar
@bot.command(name='Twite',
                description="Twite qualquer coisa.",
                brief="Twite qualquer coisa.",
                aliases=['twite','tw'],
                pass_context=False)
async def tweet(*frase):
    #frase      - Lista de palavras que foi enviada pelo usuário, ou uma fras se colocada entre aspas.
    
    tweet=''                            #Variável pra guardar a frase que vai twitar
    for palavra in frase:               #Vamos montar a frase, o discord pega as palavras separadas como argumentos       
        tweet=tweet+' '+palavra
    api.update_status(status=tweet)     #Twitamos a frase
    await bot.say('Twitado!')

#Comando para buscar um tweet
@bot.command(name='Opinião',
                description="Opinião esclarecida formada no Twitter.",
                brief="Pergunte pro zé sobre algum tema",
                aliases=['opinião','opiniao','opinie'],
                pass_context=False)
async def opina(*assunto):
    #assunto    - Sobre o que a pessoa quer saber a opinião
    
    busca=''                            
    for palavra in assunto:                      
        busca=busca+' ' + palavra

    #Vamos checar se temos buscas disponíveis
    if (api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']>0):
        tweets = tweepy.Cursor(api.search, q= busca, result_type="recent", tweet_mode='extended').items(10)
        #count      - número de tweets por página
        #lang="pt"  - Restringir a algum idioma
        
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        #Emojis não suportados são convertidos para caracteres suportados.

        opiniao=[]              #Vamos construir um vetor com os tweets
        for tweet in tweets:
            opiniao.append((tweet.full_text).translate(non_bmp_map))
            
        if (len(opiniao)==0):                               #Se ninguém twittou sobre isso
            await bot.say("Ninguém mais fala disso.")
        else:
            await bot.say(random.choice(opiniao))
    else:
        await bot.say('Estou cansado, me pergunte mais tarde.')
        
    

#Descrição do comando da aposta:
descri="Faça apostas nos jogos do dia da liga Overwatch usando uma palavra para cada time e com espaço entre os elementos, com a data opcional se não for no dia."
descri=descri+"E se tiver mais de um jogo no dia, pode especificar qual jogo.\nEx.:Para apostar no segundo jogo entre shanguai e gladiators no dia 18/07, use:\n"
descri=descri+"!aposta shanghai 3 x 0 gladiators 18/07 2.\n\nSinônimos:\n"
descri=descri+"Shanghai Dragons: shanghai,dragons,xangai dragons\n"
descri=descri+"Los Angeles Gladiators: gladiators\n"
descri=descri+"San Francisco Shock: schock,sf\n"
descri=descri+"Los Angeles Valiants: valiants\n"
descri=descri+"Dallas Fuel: dallas,fuel\n"
descri=descri+"Seoul Dynasty: seoul,seul,dynasty\n"
descri=descri+"Boston Uprising: boston,uprising\n"
descri=descri+"New York Excelsior: ny,excelsior\n"
descri=descri+"London Spitfire: london,spitfire\n"
descri=descri+"Philadelphia Fusion: philadelphia,fusion"

#Comando para apostar na liga
@bot.command(name='aposta', 
                description=descri,
                brief="Apostas do dia na Overwatch League", 
                aliases=[ 'liga','ow','overwatch'],
                pass_context=True)
async def aposta(context,time1,placar1,x,placar2,time2,*data):
    #context    - Informações sobre a mensagem que foi enviada.
    #time1      - Nome de algum time
    #placar1    - Placar correspondente a este time
    #x          - Versus
    #time2      - Nome do outro time
    #placar2    - Placar correspondente a este outro time
    #*data      - Data da aposta (opcional)

    planilha = conecta_planilha()      #Se conecta com a planilha
    
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
    await bot.say(fala)

#Comando para consultar os jogos da liga
@bot.command(name='jogos', 
                description="Consulte os jogos da lida do dia com o padrão de data 18/07. Sem informar a data, veja os jogos de hoje.",
                brief="Consulte os jogos da liga", 
                aliases=[ 'jogo'],
                pass_context=False)  
async def jogos(*data):
    #*data      - Data em que queremos ver os jogos
    planilha = conecta_planilha()      #Se conecta com a planilha
    
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
    await bot.say(partidas)
    

#Comando para consultar os jogos da liga
@bot.command(name='popularidade', 
                description="Verifique a opinião pública sobre algum tema baseado nos 10 twittes mais recentes. A nota varia de -1(negativa) a 1(positiva).",
                brief="Cheque a opinião pública sobre algo.", 
                aliases=[ 'publico'],
                pass_context=False)  
async def popularidade(*assunto):
    #assunto    - Sobre o que a pessoa quer saber a opinião

    #Línguas suportadas pelo repustate
    linguas=('ar','zh','nl','en','fr','de','he','it','ja','ko','pl','pt','ru','es','tr','th','vi')

    #vamos montar nossa expressão de busca
    busca=''                            
    for palavra in assunto:                      
        busca=busca+palavra+' ' 

    if (api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']>0):                   #Checamos se temos busca sobrando
        tweets = tweepy.Cursor(api.search, q= busca, result_type="recent", tweet_mode='extended').items(100) #Se tem buscamos

        sentimentos=[]                      #Vamos guardar as frases
        await bot.say("Deixa eu ver...")
        for tweet in tweets:                                #Vamos percorrer os tweets
            frase=(tweet.full_text).encode('utf8')          #E guardar a frase sem emoji
            if (len(frase)==0 or type(frase) != str ):      #Se não tem texto
                idioma='xx'                 #Adicionamos um codigo flaso
            else:                           #Se tem, detectamos o idioma
                idioma=detect(frase)        #Detectamos o idioma
##            if idioma in linguas:           #Se o repustate dá suporte
##                rep=client.sentiment(text=frase,lang=idioma)    #Fazemos a análise
##                if (rep['status']=='OK'):                       #Se deu certo
##                    sentimentos.append(float(rep['score']))      #Salvamos o resultado
##                
##        if (len(sentimentos)==0): #Se não tem nenhum pra análise informamos                         
##            await bot.say("Ninguém mais fala disso.")
##        else:                    #Se tem, calculamos a média
##            soma=0
##            for s in sentimentos:
##                soma=soma+s
##            media=soma/len(sentimentos)
##            if (media>0.5):
##                op='positiva.'
##            elif(media>0):
##                op='um pouco positiva.'
##            elif(media>-0,5):
##                op='um pouco negativa.'
##            else:
##                op='negativa.'
##            op="A opinião publica sobre "+busca+"é "+op
##            await bot.say(op)
        await bot.say("Acabou a cota do Repostate")

    else:                                                                                                   #Se não temos busca sobrando, avisamos
        await bot.say('Estou cansado, me pergunte mais tarde.')
    
#Criamos uma categoria de comandos
class Informativo:
    """Comandos que dão informações."""

    #Comando com informações sobre o bot
    @commands.command(brief="Sobre o bot.")
    async def info(self):
        embed = discord.Embed(title="Nome", description="Zé VI", color=0xeee657)
        embed.add_field (name="Descrição", value="Vamo esculachar!!")
        embed.add_field (name="Gmail e Twitter",value='zeromildobot@gmail.com  ')
        embed.add_field (name="Versão",value='Infinita Highway')
        await bot.say(embed=embed)

#Adicionamos os comandos da categora informativo
bot.add_cog(Informativo())

#RODAR O BOT----------------------------------------------------------------------------------------------------------------
bot.run(token)
