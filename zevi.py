##ZÉ VI
##Desenvolvido por:     Jhordan Silveira de Borba
##E-mail:               jhordandecacapava@gmail.com
##Website:              https://sapogithub.github.io
##Mais informações:     https://github.com/SapoGitHub/Repositorio-Geral/wiki/Zé-VI
##2018

import random                       #Biblioteca para comandos aleatorios
import discord                      #Biblioteca para trabalhar com o discord
from discord.ext import commands
import tweepy   #Biblioteca para lidar com o Twitter
import json     #Biblioteca para lidar com o JSON
import sys      #Módulo que prove recursos relacionados ao interpretador

#CREDENCIAIS----------------------------------------------------------------------------------------------------------------

token=                  'NDY4ODI1OTAwNzQ2NTM5MDA4.Di_TaQ.kP42Lt9eXkyMfMB_1w2p2YKq9wM'       #Token
consumer_key =          'BOAs4wfRHO5ShFjojLPzLdK3B'                                         #Consumer Key (API Key)
consumer_secret=        'BUcAlFriglp6RkLzVvkZ8b3zYUNLtqvAwGGWs7YudLLQWnO1Gi'                #Consumer Secret (API Secret)
access_token=           '1019318137605513218-UzaJyIKGjSL8EQ6fta4L5BlhnFRytJ'                #Access Token
access_token_secret=    'M5fauDKnuJt3yC3RdxMM7Wr1NFBzhruuc51DGo21nbSk0'                     #Access Token Secret

#COFIGURAÇÃO DISCORD---------------------------------------------------------------------------------------------------------
bot = commands.Bot(command_prefix='!', description='Vamo esculachar!!!')

#Vamos printar quando conectar ao discord
@bot.event
async def on_ready():
    print('Logado como:')
    print(bot.user.name)

#CONEXÃO TWITTER-------------------------------------------------------------------------------------------------------------
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#COMANDOS--------------------------------------------------------------------------------------------------------------------
#Comando da Bola 8
@bot.command(name='bola8', #Como pode ser chamado a funçaõ no discord
                description="Faça uma pergunta que possa ser respondida com sim ou não.", #Descrição que aparece no !help bola8
                brief="Respostas sim/não.", #Descrição que aparece no !help
                aliases=['bola_oito', 'bolaoito'], #Outras formas de chamar a mesma função
                pass_context=True)  #Se vai passar o contexto
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
    

#Criamos uma categoria de comandos
class Informativo:
    """Comandos que dão informações."""

    #Comando com informações sobre o bot
    @commands.command(brief="Sobre o bot.")
    async def info(self):
        embed = discord.Embed(title="Nome", description="Zé VI", color=0xeee657)
        embed.add_field (name="Descrição", value="Vamo esculachar!!")
        embed.add_field (name="Gmail e Twitter",value='zeromildobot@gmail.com:zeromildao')
        await bot.say(embed=embed)

#Adicionamos os comandos da categora informativo
bot.add_cog(Informativo())

#ZONA DE TESTES FORA DO DISCORD---------------------------------------------------------------------------------------------

#RODAR O BOT----------------------------------------------------------------------------------------------------------------
bot.run(token)
