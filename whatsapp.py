##ZÉ VI: Módulo WhatsApp
##Desenvolvido por:     Jhordan Silveira de Borba
##E-mail:               jhordandecacapava@gmail.com
##Website:              https://sapogithub.github.io
##Mais informações:     https://github.com/SapoGitHub/Ze-VI/wiki
##2018

import discord                                                      #Biblioteca para trabalhar com o discord
from WFAPI import *     #Importamos as funções relacionadas ao WFAPI

#Funçao para obter o QR code
def whatsapp_qr(driver):
    #driver         - Conexão com o Chrome
    
    return gerar_qr(driver)

#Função para enviar mensagem
def whatsapp_whats(driver, destinatario,*mensagem):
    #driver         - Conexão com o Chrome
    #destinatario   - Quem deve receber nossa mensagem
    #*mensagem      - Vetor com as palavras da nossa frase
    
    frase=''                            #Variável pra guardar a frase que vai twitar
    for palavra in mensagem:            #Vamos montar a frase, o discord pega as palavras separadas como argumentos       
        frase=frase+' '+palavra

    try:
        enviar_msg(driver,destinatario,frase)   #Chamamos a função para enviar a mensagem
        return ('Mensagem enviada!')            #Se tivemos sucesso informamos
    except:
        return ('Tente de novo.')               #Se encontramos um erro reportamos

    
#Função para checar quem nos enviou novas mensagens
def whatsapp_mensagens(driver,tamanho_max):
    #driver         - Conexão com o Chrome
    #tamanho_max    - Quantidade de contatos e grupos

    try:           #Tentamos checar
        contatos=novas_msgs(driver,tamanho_max) #Pegamos quem nos enviou novas mensagens
        texto='Novas mensagens de: '             #Montamos nosso texto
        for contato in contatos:
            texto=texto+contato+', '

        if (len(contatos)>0):                   #Se alguém nos enviou
            return texto                        #Retornamos a mensagem
        else:
            return ('Sem novas mensagens.')     #Ou avisamos que não há novas
    except:
       return ('Tente de novo.')           #Ou ainda avisamos que não conseguimso checar


#Função para checar as últimas mensagens sem respostas de algum contato
def whatsapp_contato(driver,contato):
    #driver         - Conexão com o Chrome
    #contato        - De quem queremos ver que mensagens recebemos

    try:                                        #Vamos tentar
        mensagens=ult_msgs(driver,contato)      #Recebemos as últimas mensagens do contato
        driver.get("https://web.whatsapp.com")  #Reabrimos a pagina para não ficar em nenhuma conversa aberta

        texto=contato+':\n'                     #Vamos montar as mensagens
        tam=len(mensagens)
        for n in range(tam-1,-1,-1):
            texto=texto+mensagens[n]+'\n'
        
        if (len(mensagens)>0):                  #Se temos mensagens não respondidas
            return texto                        #Retornamos as mensagens
        else:                                   #Ou então retornamos que não há mensagens
            return ('Sem mensagens não respondidas.')
    except:
        return ('Tente de novo.')               #Ou ainda avisamos que não conseguimos

print ('Módulo do WhatsApp importado.')
