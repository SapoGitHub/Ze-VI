##ZÉ VI
##Desenvolvido por:     Jhordan Silveira de Borba
##E-mail:               jhordandecacapava@gmail.com
##Website:              https://sapogithub.github.io
##Mais informações:     https://github.com/SapoGitHub/Ze-VI/wiki
##2018

import discord                                                      #Biblioteca para trabalhar com o discord
from discord.ext import commands                                    
import tweepy                                                       #Biblioteca para lidar com o Twitter
import os                                                           #Biblioteca para lidar com o Sistema Operacional
from repustate import Client                                        #Biblioteca para fazer análise de sentimento
import json                                                         #Biblioteca para lidar com o JSON
import gspread                                                      #Biblioteca para lidar com planilhas
from oauth2client.service_account import ServiceAccountCredentials  #Biblioteca para gerar credenciais do tipo OAuth utilizadas pelo google
from selenium import webdriver                                      #Biblioteca de automatização de tarefas no navegador
from selenium.webdriver.chrome.options import Options
from WFAPI import *                                                 #Importamos as funções relacionadas ao WFAPI

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

#CONEXÃO REPUSTATE----------------------------------------------------------------------------------------------------------
client = Client(api_key=api_key, version='v4')
print("Conectado ao Repustate.")

#CONEXÃO GOOGLE--------------------------------------------------------------------------------------------------------------

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

conecta_planilha(login)     #Testamos a conexão

#CONFIGURAÇÃO WHATSAPP------------------------------------------------------------------------------------------------------
#Vamos configurar a inicialização do Google Chrome Headless no Heroku
chrome_options = Options()
chrome_options.binary_location = os.environ['GOOGLE_CHROME_BIN']
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--headless')
#Precisamos ainda configurar o user-agent para o WhatsApp em especifico funcionar
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36")
driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], chrome_options=chrome_options)

#Minha lista de contatos que converso
agenda=['Vô','Amor','Paloma','Vinicius','Vó','Mãe','Pai','Gra','Bruno',
        'Flanarte','Giovani','Psico Darlen Vaz','Pedro','Zardo','Felipe',
        'Geferson','Juan','Roger','Rafael','André Smaria','mi','Guga']

#Grupos que faço parte
grupos=['Nossa prole','Ahiba']

#Quantidade máxima de conversas
tamanho_max=len(agenda)+len(grupos)

nomes=[]        #Nomes dos contatos que enviaram mensagens
mensagens=[]    #Mensagens enviadas pelos contatos

print('Conectado ao Chrome.')
#COMANDOS--------------------------------------------------------------------------------------------------------------------
from twitter import *               #Importamos as funções relacionadas ao twitter
from owl import *                   #Importamos as funções relacionadas à liga overwatch
from whatsapp import *              #Importamos as funções relacionadas ao whatsapp

#Categoria do Twitter
class Twitter:
    """Comandos que fazem uso do Twitter."""
    #Comando para twittar
    @commands.command(name='Twite',
                description="Twite qualquer coisa.",
                brief="Twite qualquer coisa.",
                aliases=['twite','tw'],
                pass_context=False)
    async def tweet(self,*frase):
        await bot.say (twitter_tweet(api,frase))

    #Comando para buscar um tweet
    @commands.command(name='Opinião',
                description="Opinião esclarecida formada no Twitter.",
                brief="Pergunte pro zé sobre algum tema",
                aliases=['opinião','opiniao','opinie'],
                pass_context=False)
    async def opina(self,*assunto):
        await bot.say(twitter_opina(api,assunto))

    #Comando para a opinião pública sobre algum assunto
    @commands.command(name='popularidadebr', 
                description="Verifique a opinião pública em português sobre algum tema baseado nos 10 twittes mais recentes. A nota varia de -1(negativa) a 1(positiva).",
                brief="Cheque a opinião pública BR sobre algo.", 
                aliases=[ 'publico','popularidade'],
                pass_context=False)  
    async def popularidade(self,*assunto):
        await bot.say(twitter_popularidade(api,client,assunto))

#Salvamos os comandos
bot.add_cog(Twitter())


#Categoria da liga
class OWL:
    """Comandos relacionados à Overwatch League"""
    
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
    @commands.command(name='aposta', 
                    description=descri,
                    brief="Apostas do dia na Overwatch League", 
                    aliases=[ 'liga','ow','overwatch'],
                    pass_context=True)
    async def aposta(self,context,time1,placar1,x,placar2,time2,*data):
        planilha = conecta_planilha(login)
        await bot.say(owl_aposta(context,planilha,time1,placar1,x,placar2,time2,*data))

    #Comando para consultar os jogos da liga
    @commands.command(name='jogos', 
                    description="Consulte os jogos da lida do dia com o padrão de data 18/07. Sem informar a data, veja os jogos de hoje.",
                    brief="Consulte os jogos da liga", 
                    aliases=[ 'jogo'],
                    pass_context=False)  
    async def jogos(self,*data):
        planilha = conecta_planilha(login)
        await bot.say(owl_jogos(planilha,*data))

bot.add_cog(OWL())

#Categoria do Whatsapp
class WhatsApp:
    """Comandos que fazem uso do WhatsApp."""
    #Comando para gerar o QR Code
    @commands.command(name='qr',
                description="Obter o QR Code.",
                brief="Obter o QR Code.",
                aliases=['QR','qr_code','QR_code'],
                pass_context=True)
    async def qr(self,context):
        await bot.send_file (context.message.author,whatsapp_qr(driver))

    #Comando para enviar mensagem
    @commands.command(name='whats',
                description="Comando para enviar mensagem para o WhatsApp",
                brief="Envie mensagem pelo whats",
                aliases=['whatsapp','Whats','WhatsApp'],
                pass_context=True)
    async def whats(self,context,destinatario,*mensagem):
        try:
            status=whatsapp_whats(driver, destinatario,*mensagem)
        except:
            status=False

        print(status)
        if (status==True):
            await bot.say ('Mensagem enviada.')
        else:
            await bot.say ('Tente de novo.')

    #Comando para checar se temos novas mensagens no WhatsApp
    @commands.command(name='mensagens',
                description="Comando para checar novas mensagens no WhatsApp",
                brief="Receba as mensagens do WhatsApp",
                aliases=['novas_mensagens'],
                pass_context=True)
    async def mensagens(self,context):
        try:
            contatos=whatsapp_mensagens(driver,tamanho_max)
            await bot.say (contatos)
        except:
            await bot.say ('Tente de novo.')
        
    #Comando para ver as ultimas mensagens sem respostas de um contato
    @commands.command(name='contato',
                description="Comando para checar ultimas mensagens de algum contato no WhatsApp",
                brief="Receba as ultimas mensagens de alguém no WhatsApp",
                aliases=['Contato'],
                pass_context=True)
    async def contato(self,context,contato):
        try:
            mensagem=whatsapp_contato(driver,contato)
            await bot.say (mensagem)
        except:
            await bot.say('Tente de novo.')
 
                
#Salvamos os comandos
bot.add_cog(WhatsApp())

#Comandos sem categoria
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
    

#Comando com informações sobre o bot
@bot.command(brief="Sobre o bot.")
async def info():
    embed = discord.Embed(title="Nome", description="Zé VI", color=0xeee657)
    embed.add_field (name="Descrição", value="Vamo esculachar!!")
    embed.add_field (name="Gmail e Twitter",value='zeromildobot@gmail.com  ')
    embed.add_field (name="Versão",value='Spelunky é um jogão!')
    await bot.say(embed=embed)

#RODAR O BOT----------------------------------------------------------------------------------------------------------------
bot.run(token)
