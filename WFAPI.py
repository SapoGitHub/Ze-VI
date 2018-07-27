##ZÉ VI: Biblioteca WFAPI
##Desenvolvido por:     Jhordan Silveira de Borba
##E-mail:               jhordandecacapava@gmail.com
##Website:              https://sapogithub.github.io
##Mais informações:     https://github.com/SapoGitHub/Ze-VI/wiki
##2018

from selenium import webdriver                          #Biblioteca de automatização de tarefas no navegador
from selenium.webdriver.common.keys import Keys         #Importa os atalhos de teclas do Selenium
from PIL import Image                                   #Biblioteca para tratamento de imagem
import time

#Função para definir o máximo possivel de conversas a serem carregadas
def tamanho(driver,tamanho_max):
        n=0     #Contador
        for x in range(1,(tamanho_max+1)):   
                caminho='//*[@id="pane-side"]/div/div/div/div['+str(x)+']'      #Caminho para o div mais alto de um contato na lista de conversas
                try:                                                            
                        elemento = driver.find_element_by_xpath(caminho)        #Se o elemento existe
                        n=n+1                                                   #Adicionamos o contador
                except:                 #Se não existe                                    
                        return n        #Retornamos
        return n

#Função pra gerar o QR  code
def gerar_qr(driver):
        driver.get("https://web.whatsapp.com")  #Abrimos a pagina do WhatsApp Web
        nimg='qr.png'                           #Nome da imagem a ser salvo
        driver.get_screenshot_as_file(nimg)     #Screenshot do navegador
        #im = Image.open(nimg)                   #Abre a imagem
        #im.crop((656,132,960,436)).save(nimg)   #Corta a imagem 
        return nimg

#Função para abrir a conversa pela pesquisa -- DEPRECIADO
def abrir_conversa_pesquisa(driver,tamanho_max,contato):
        #contato   - Quem vamos abrir as mensagens

        caminho='//*[@id="side"]/div[2]/div/label/input'        #Caminho para "Procurar ou começar uma nova conversa"
        elemento = driver.find_element_by_xpath(caminho)        #Pegamos o elemento
        elemento.clear()                                        #Limpamos caso tenha alguma pesquisa antiga
        elemento.send_keys(contato)                             #Digitamos o destinatário
        time.sleep( 5 )                                         #Esperamos para fazer a busca
        n=tamanho(driver,tamanho_max)                                             #Tamanho max
        for x in range(1,n+1):   #Checamos todos possíveis resultados
                caminho='//*[@id="pane-side"]/div/div/div/div['+str(x)+']/div/div/div[2]/div[1]/div[1]/span/span'       #Caminho para o nome do contato
                try:                                                                                                    #Tentamos checar o resultado
                        elemento = driver.find_element_by_xpath(caminho)                                                #Pegamos o elemento
                        if (elemento.get_attribute('title')==contato):                                                  #Comparamos o nome com o nosso objetivo
                                caminho='//*[@id="pane-side"]/div/div/div/div['+str(x)+']/div/div'                      #Se for, salvamos o caminho pro elemento do resultado
                                break                                                                                   #E saímos do for
                except:                                                                                                 #Se não funcionar
                        pass                                                                                            #Tentamos o próximo resultado
        elemento = driver.find_element_by_xpath(caminho)                        #Pegamos o elemento
        elemento.click()                                                        #Clicamos
        caminho='//*[@id="side"]/div[2]/div/button'                             #Caminho para o botão de voltar
        elemento = driver.find_element_by_xpath(caminho)                        #Pegamos o elemento
        elemento.click()                                                        #Clicamos
        return

#Função para abrir conversa pela busca de contatos
def abrir_conversa(driver,contato):
        #contato   - Quem vamos abrir as mensagens
        
        time.sleep(3)                                           #Aguardar um tempo
        caminho='//*[@id="side"]/header/div[2]/div/span/div[2]' #Caminho para o botão de nova conversa
        elemento = driver.find_element_by_xpath(caminho)        #Pegamos o elemento
        elemento.click()                                        #Clicamos
        time.sleep(3)
        caminho='//*[@id="app"]/div/div/div[1]/div[1]/span/div/span/div/div[1]/div/label/input'      #Caminho para o campo de digitação
        elemento = driver.find_element_by_xpath(caminho)        #Pegamos o elemento
        elemento.send_keys(contato)                             #Digitamos o destinatário
        time.sleep(1)                                           #Aguardamos mais um pouco
        caminho='//*[@id="app"]/div/div/div[1]/div[1]/span/div/span/div/div[2]/div'        #Caminho para o primeiro resultado
        elemento = driver.find_element_by_xpath(caminho)        #Pegamos o elemento
        elemento.click()                                        #Clicamos
        return

#Função para enviar mensagem
def enviar_msg(driver,destinatario,msg):
        #destinatario   - Quem vai receber a mensagem
        #msg            - Mensagem a ser enviada

        while (True):
                try:
                        global intervalo
                        intervalo=60
                        time.sleep(5)
                        abrir_conversa(driver,destinatario)                                            #Abrimos a conversa de quem vamos enviar
                        caminho='//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'               #Caminho da conversa
                        elemento = driver.find_element_by_xpath(caminho)                        #Selecionamos o campo da mensagem
                        elemento.clear()                                                        #Limpamos caso tenha alguma coisa antiga
                        elemento.send_keys(msg,Keys.ENTER)                                      #Enviamos a mensagem
                        time.sleep( 5 )                                         #Aguardamos enviar
                        driver.get("https://web.whatsapp.com")  #Reabrimos a pagina para não ficar em nenhuma conversa aberta
                        intervalo=1
                        return
                except:
                        print('Tentando enviar novamente.')

#Função para lermos as ultimas mensagens enviadas de algum contato:
def ult_msgs(driver,contato):
        time.sleep(1)   
        abrir_conversa(driver,contato)     #Abrimos a conversa
        time.sleep(3) 
        #Checamos se tem mais mensagem ou não
        cam='//*[@id="main"]/div[2]/div/div/div[2]/div'
        elemento = driver.find_element_by_xpath(cam)
        titulo=elemento.get_attribute('title')
        if (titulo == 'Carregar mensagens recentes'):
            ide=3
        else:
            ide=2

        #Precisamos saber quantas mensagens foram carregadas
        n=0
        classes=[]
        msg=[]
        for x in range(1,2000):
            cam='//*[@id="main"]/div[2]/div/div/div['+str(ide)+']/div['+str(x)+']'
            try:
                elemento = driver.find_element_by_xpath(cam)
                n=n+1
                cam='//*[@id="main"]/div[2]/div/div/div['+str(ide)+']/div['+str(x)+']/div'
                try:
                        elemento = driver.find_element_by_xpath(cam)
                        classe = elemento.get_attribute('class')
                        try:
                                cam='//*[@id="main"]/div[2]/div/div/div['+str(ide)+']/div['+str(x)+']/div/div/div[1]/div/span'
                                elemento = driver.find_element_by_xpath(cam)
                                texto=elemento.text
                                msg.append(texto)
                                classes.append(classe)
                        except:
                                #print('Problemas em pegar o texto.')
                                pass
                except:
                        #print('Problemas em pegar a classe')
                        pass
            except:
                #print('Não há mais mensagens novas')
                break
        qt=len(classes)
        final=[]
        #print(msg)
        #print(classes)
        for x in range(qt-1,0,-1):
                if ('message-in' in classes[x]):
                        final.append(msg[x])        
                else:
                        break

        return final


#Função para checar se tem novas mensagens não lidas
def novas_msgs(driver,tamanho_max):
        contatos=[]             #Onde vamos guardar quem nos enviou as mensagens não lidas
        n=tamanho(driver,tamanho_max)             #Tamanho max

        for x in range(1,n+1):  #Checar todos contatos carregados na lista de conversa
                try:            #Checamos se tem mensagem nova
                        caminho='//*[@id="pane-side"]/div/div/div/div['+str(x)+']/div/div/div[2]/div[2]/div[2]/span[1]/div'     #Caminho para a quantidade de mensagens novas
                        elemento = driver.find_element_by_xpath(caminho)                                                        #Verificamos se existe o elemento
                        caminho='//*[@id="pane-side"]/div/div/div/div['+str(x)+']/div/div/div[2]/div[1]/div[1]/span/span'       #Caminho para o nome do contato
                        elemento = driver.find_element_by_xpath(caminho)                                                        #Pegamos o elemento
                        contatos.append(elemento.get_attribute('title'))                                                        #Salvamos o nome
                except:         #Se não existe o elemento de novas mensagens do contato
                        pass    #Passamos e checamos todas as novas mensagens na lista

        #E então pegar as novas mensagens
        nvas_msgs=[]
        for contato in contatos:
            msgs=ult_msgs(driver,contato)         
            nvas_msgs.append(msgs)
            
        driver.get("https://web.whatsapp.com")  #Reabrimos a pagina para não ficar em nenhuma conversa aberta
        time.sleep(3)                           #Espera
        return(contatos,nvas_msgs)
