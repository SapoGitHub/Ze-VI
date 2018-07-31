# ZÉ VI

Para a criação do bot, foi necessário a criação de um aplicativo no [discord](https://discordapp.com/developers/applications/), assim como também a criação de outro aplicativo no [Twitter](https://apps.twitter.com) foi necessário para realizar a integração com o mesmo. No caso do Twitter, ainda precisamos gerar nossos token de acesso (Access Token e Access Token Secret).

Depois disso, um terceiro aplicativo foi criado no [Heroku](https://dashboard.heroku.com/apps/) unicamente para colocarmos nosso bot 24h/dia online na nuvem. Dentro do Heroku, utilizamos variáveis de ambiente para guardar as informações sensíveis de acesso. 

Ainda além dos aplicativos também criamos um projeto no [Google APIs](https://console.developers.google.com/apis/dashboard?), onde ativamos o Google Drive API e Google Sheets API, ainda geramos uma credencial do tipo "Chave da conta de serviço" do tipo "JSON". Depois precisamos pegar o "client_email" dentro deste arquivo JSON e compartilharmos com ele a planilha que queremos ter acesso.

Esse é um bot desenvolvido para meu pessoal, por isso alguns recursos se restringem a um máximo de 3 usuários específicos definidos no próprio código por exemplo, para ser utilizado em servidores maiores é necessário realizar as devidas adaptações.

## Módulo da OWL

Utiliza as APIs do Google para conectar e editar as planilhas do Google. O bolão é salvo com o seguinte padrão:

![imagem do bolão](https://github.com/SapoGitHub/Ze-VI/blob/master/imagens/bolao.png)

<code>!aposta time1 placar1 x placar2 time2 dd/mm</code>

Registra a aposta em um bolão salvo em uma planilha no Google Docs. Caso a data não seja informada, é considerado que o dia atual, e ainda caso haja dois jogos no mesmo dia, é necessário informar explicitamente qual jogo é, caso esteja apostando no segundo jogo. 

Ex.:
- Se quiser apostar em um segundo jogo entre Shanghai Dragons e New York Excelsior: <code>!aposta shanghai 4 x 1 excelsior 30/7 2</code>;
- Se for o primeiro jogo, ou o único do dia, pode ser apenas:  <code>!aposta shanghai 4 x 1 excelsior 30/7</code>;
- E se o jogo ainda for no dia atual:  <code>!aposta shanghai 4 x 1 excelsior</code>.

<code>!jogos dd/mm</code>

Informa os jogos que acontecerão na data informada. Caso nenhuma data seja informada, considera-se o dia atual.

## Módulo do Twitter

Utiliza-se o API do Twitter para buscar tuites e tuitar, e o API do repustate para fazer análises de sentimento.

<code>!Twite "frase" </code>
	
Tuita a frase no perfil dono do API do Twitter.

<code>!Opinião "tópico"</code>

O bot busca e reproduz um tuite aleatório com o tópico informado.

<code>!popularidadebr "tópico"</code>

Realiza análise de sentimento em uma porção de tuites sobre o tópico informado e então a partir da média dos resultados, retorna uma resposta.

## Módulo WhatsApp

Vamos utilizar o nosso WFAPI para integrarmos ao WhatsApp

<code>!qr</code>

Envia o QR Code para conexão ao Web WhatsApp para o usuário, ou caso já esteja conectado, um recorte na tela na posição equivalente. Podendo então, também ser usada para conferir a conexão com o mesmo.

<code>!mensagens</code>

Receba o nome de usuários que lhe enviaram novas mensagens.

<code>!contato "contato"</code>

Receba as últimas mensagens sem resposta enviados pelo contato para você.

<code>!whats contato "mensagem"</code>

Envie uma mensagem para o contato em questão.

### Observações

O módulo do WhatsApp tem algumas limitações conhecidas:
- Todas mencionadas no [WFAPI](https://github.com/SapoGitHub/Repositorio-Geral/tree/master/WFAPI);
- Só pode conectar um usuário ao WhatsApp Web por vez;
- Só pode checar novas mensagens por comando;
- Problema quando reabrimos o bot e não foi removido a conexão com o WhatsApp web anterior;
- Visualiza a conversa com o contato enquanto envia a mensagem para o mesmo.
- Esperar as repostas dos comandos antes de enviar um novo;
- Não enviar muitas mensagens ao mesmo tempo. 
	- Alternativa: enviar uma mensagen grande ou com quebra de linha dentro de aspas.
	- Ex.:<code>!whats destinatário "Mensagem 1 \n Mensagem 2"</code>.
- Se desconecta depois de algum tempo de inatividade.

Melhorias possíveis:
- Expandir para a utilização de até três usuários simultâneos.
- Checar ultimas mensagens do contato antes de enviar nova;
- Agendar o envio de mensagens;
- Realizar a transcrição de áudios;
- Realizar a conversão de texto para áudio.

Recomendações:
- Enviar mensagens entre aspas (<code>!whats contato "mensagem completa"</code>);
- Não estar recebendo novas mensagens enquanto checa novas mensagens na conversa.

## Outros comandos

<code>!info</code>

Retorna informações sobre o bot.

<code>!bola8 "pergunta"</code>

Retorna uma resposta aleatória do tipo "sim" ou "não" para a pergunta proposta.
