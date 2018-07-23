##ZÉ VI: Módulo Twitter
##Desenvolvido por:     Jhordan Silveira de Borba
##E-mail:               jhordandecacapava@gmail.com
##Website:              https://sapogithub.github.io
##Mais informações:     https://github.com/SapoGitHub/Ze-VI/wiki
##2018

import random                                                       #Biblioteca para comandos aleatorios
import tweepy                                                       #Biblioteca para lidar com o Twitter
import sys                                                          #Biblioteca que prove recursos relacionados ao interpretador
from langdetect import detect                                       #Biblioteca para detectar língua sem limite

#Comando para twittar
def twitter_tweet(api,frase):
    #api        - API do Twitter
    #frase      - Lista de palavras que foi enviada pelo usuário, ou uma fras se colocada entre aspas.    

    tweet=''                            #Variável pra guardar a frase que vai twitar
    for palavra in frase:               #Vamos montar a frase, o discord pega as palavras separadas como argumentos       
        tweet=tweet+' '+palavra
    api.update_status(status=tweet)     #Twitamos a frase
    return ('Twitado!')


#Comando para buscar um tweet
def twitter_opina(api,assunto):
    #api        - API do Twitter
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
            return ("Ninguém mais fala disso.")
        else:
            return (random.choice(opiniao))
    else:
        return ('Estou cansado, me pergunte mais tarde.')

#Comando para consultar a opinião pública sobre algum assunto
    
def twitter_popularidade(api,client,assunto):
    #api        - API do Twitter
    #client     - Conexão do Repustate
    #assunto    - Sobre o que a pessoa quer saber a opinião

    serv='Repustate-pt'    #Serviço de análise que vamos usar: Repustate, Google
    busca=''            #vamos montar nossa expressão de busca                            
    for palavra in assunto:                      
        busca=busca+palavra+' ' 
    
    if (api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']>0):                   #Checamos se temos busca sobrando        
        if (serv=='Repustate-pt'):      #Repustate pesquisando somente em pt
            idioma='pt'                 #Idioma
            tweets = tweepy.Cursor(api.search, q= busca, result_type="recent", lang=idioma,tweet_mode='extended').items(100) #Se tem buscamos
            frases=[]                           #Vamos guardar as frases
            sentimentos=[]                      #Vamos guardar os sentimentos
            for tweet in tweets:                #Vamos percorrer os tweets
                frases.append(tweet.full_text)  #E guardar as frases               
            try:
                rep=client.bulk_sentiment(frases,lang=idioma)    #Fazemos a análise
            except:
                return ("Acabou minha cota de análise.")  #Ou avisamos que acabou a cota            
            if (rep['status']=='OK'):                       #Se deu certo
                for n in range(len(frases)):
                    ide='text'+str(n)                       #anotamos o id do nosso texto
                    sentimentos.append(float(rep['results'][ide]))#Salvamos o resultado
                    
        elif(serv=='Repustate'):    #Pesquisando em qualquer idioma com Repustate
            #Línguas suportadas pelo repustate
            linguas=('ar','zh','nl','en','fr','de','he','it','ja','ko','pl','pt','ru','es','tr','th','vi')
            tweets = tweepy.Cursor(api.search, q= busca, result_type="recent", tweet_mode='extended').items(10) #Se tem buscamos
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd) #Emojis não suportados são convertidos para caracteres suportados. 
            sentimentos=[]                      #Vamos guardar as frases
            for tweet in tweets:                                #Vamos percorrer os tweets
                frase=(tweet.full_text).translate(non_bmp_map)  #E guardar a frase sem emoji            
                try:                            #Tentamos detectar o idioma
                    idioma = detect(frase)
                except:
                    idioma="xx"                 #Se não guardamos um idioma falso
                if idioma in linguas:           #Se o repustate dá suporte
                    try:
                        rep=client.sentiment(text=frase,lang=idioma)    #Fazemos a análise
                    except:
                        return ("Acabou minha cota de análise.")  #Ou avisamos que acabou a cota
                    if (rep['status']=='OK'):                       #Se deu certo
                        sentimentos.append(float(rep['score']))      #Salvamos o resultado
      
        else:
            print("Ainda não configurado.")
                                    
        if (len(sentimentos)==0): #Se não tem nenhum pra análise informamos                         
            return ("Ninguém mais fala disso.")
        else:                    #Se tem, calculamos a média
            soma=0
            for s in sentimentos:
                soma=soma+s
            media=soma/len(sentimentos)
            if (media>0.5):
                op='positiva.'
            elif(media>0):
                op='um pouco positiva.'
            elif(media>-0,5):
                op='um pouco negativa.'
            else:
                op='negativa.'
            op="A opinião publica sobre "+busca+"é "+op
            return (op)
    else:                                                                                                   #Se não temos busca sobrando, avisamos
        return ('Estou cansado, me pergunte mais tarde.')


print ("Módulo do Twitter importado.")
