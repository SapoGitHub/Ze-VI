##ZÉ VI
##Desenvolvido por:     Jhordan Silveira de Borba
##E-mail:               jhordandecacapava@gmail.com
##Website:              https://sapogithub.github.io
##Mais informações:     https://github.com/SapoGitHub/Ze-VI/wiki
##2018

import random                       #Biblioteca para comandos aleatorios
import discord                      #Biblioteca para trabalhar com o discord
from discord.ext import commands
import tweepy   #Biblioteca para lidar com o Twitter
import json     #Biblioteca para lidar com o JSON
import sys      #Módulo que prove recursos relacionados ao interpretador
import os       #Biblioteca para lidar com o Sistema Operacional
import gspread                                                      #Biblioteca para lidar com planilhas
from oauth2client.service_account import ServiceAccountCredentials  #Biblioteca para gerar credenciais do tipo OAuth utilizadas pelo google
import datetime                                                     #Biblioteca com funções relacionadas ao tempo

#DADOS SENSÍVEIS----------------------------------------------------------------------------------------------------------------

token = os.environ['token']                                 #Token
consumer_key = os.environ['consumer_key']                   #Consumer Key (API Key)
consumer_secret = os.environ['consumer_secret']             #Consumer Secret (API Secret)
access_token = os.environ['access_token']                   #Access Token
access_token_secret = os.environ['access_token_secret']     #Access Token Secret

login = {                                                                                   #Dados do API do Google
    "type": os.environ['type'],
    "private_key_id": os.environ['private_key_id'],
    "private_key": os.environ['private_key'],
    "client_email": os.environ['client_email'],
    "client_id": os.environ['client_id'],
    }

#COFIGURAÇÃO DISCORD---------------------------------------------------------------------------------------------------------
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
#Precisamos usar o scope ao adquirir um token de acesso
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#Obtemos as credenciais
credenciais = ServiceAccountCredentials.from_json_keyfile_dict(login, scope)

google = gspread.authorize(credenciais)     #Conectamos
planilha = google.open("Bolão OWL").sheet1      #Abrimos a pagina 1 do arquivo
print("Conectado à planilha.")

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
        tweets = tweepy.Cursor(api.search, q= busca, result_type="recent", tweet_mode='extended').items(1)
        #count      - número de tweets por página
        #lang="pt"  - Restringir a algum idioma
        
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        #Emojis não suportados são convertidos para caracteres suportados.

        opiniao='Não tenho opinião, ninguém fala disso.'
        for tweet in tweets:
            opiniao=(tweet.full_text).translate(non_bmp_map)
            
    else:
        opiniao='Estou cansado, me pergunte mais tarde.'
        
    await bot.say(opiniao)

#Descrição do comando da aposta:
descri="Faça apostas nos jogos do dia da liga Overwatch usando uma palavra para cada time e com espaço entre os elementos.\nEx.: shangai 3 x 0 gladiators.\n\nSinônimos:\n"
descri=descri+"Shanghai Dragons: shanghai,dragons,xangai dragons\n"
descri=descri+"Los Angeles Gladiators: gladiators\n"
descri=descri+"San Francisco Shock: schock,sa\n"
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
                brief="Apostas do dia na Overwatch League", #Descrição que aparece no !help
                aliases=[ 'liga','ow','overwatch'], #Outras formas de chamar a mesma função
                pass_context=True)  #Se vai passar o contexto
async def aposta(context,time1,placar1,x,placar2,time2):
    #context    - Informações sobre a mensagem que foi enviada.

    apostador=str(context.message.author) #Para sabermos quem esta apostando
    
    #Dicionários que vamos utilizar
    dsem = {"1":"SEG","2":"TER","3":"QUA","4":"QUI","5":"SEX","6":"SAB","7":"DOM"} #Dias da semana
    times = {   #Sinônimos para os nomes dos times
        "Shanghai Dragons":("shanghai","dragons","xangai dragons","shangai"),
        "Los Angeles Gladiators":("gladiators"),
        "San Francisco Shock":("schock","sa"),
        "Los Angeles Valiants":("valiants"),
        "Dallas Fuel":("dallas","fuel"),
        "Seoul Dynasty":("seoul","seul","dynasty"),
        "Boston Uprising":("boston","uprising"),
        "New York Excelsior":("ny","excelsior"),
        "London Spitfire":("london","spitfire"),
        "Philadelphia Fusion":("philadelphia","fusion")}
    nos={"ZéRomildo#1325":5,"Fitz#0746":6,"Sapo#0431":7}    #Nossa localização na tabela

    #Vamos pegar o dia atual
    dia = dsem[datetime.date.today().strftime("%w")]+ " - " + datetime.date.today().strftime("%d") +"/"+datetime.date.today().strftime("%m")

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

    #Então podemos percorrer cada um dos elementos:
    for jogo in jogos:
        #E checar se o jogo desse dia é o que nos interessa:
        if ((planilha.cell(jogo.row, jogo.col+1).value == timeshj[0] or planilha.cell(jogo.row, jogo.col+1).value == timeshj[1])
            and
            (planilha.cell(jogo.row, jogo.col+3).value == timeshj[0] or planilha.cell(jogo.row, jogo.col+3).value == timeshj[1])):
            linha=jogo.row  #Se é retornamos a linha
            break

    #Com a linha vamos montar nossa aposta, primeiro precisamos saber a ordem
    if (planilha.cell(linha, 2).value==timeshj[0]):
        aposta=placar1+' x '+placar2
    else:
        aposta=placar2+' x '+placar1

    #Agora precisamos salvar a aposta, dependendo de quem apostou
    planilha.update_cell(linha, nos[apostador], aposta)

    await bot.say("Aposta feita!")
    

#Criamos uma categoria de comandos
class Informativo:
    """Comandos que dão informações."""

    #Comando com informações sobre o bot
    @commands.command(brief="Sobre o bot.")
    async def info(self):
        embed = discord.Embed(title="Nome", description="Zé VI", color=0xeee657)
        embed.add_field (name="Descrição", value="Vamo esculachar!!")
        embed.add_field (name="Gmail e Twitter",value='zeromildobot@gmail.com  ')
        embed.add_field (name="Versão",value='21')
        await bot.say(embed=embed)

#Adicionamos os comandos da categora informativo
bot.add_cog(Informativo())

#RODAR O BOT----------------------------------------------------------------------------------------------------------------
bot.run(token)
