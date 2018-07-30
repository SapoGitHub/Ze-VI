# Z� VI


Para a cria��o do bot, foi necess�rio a cria��o de um aplicativo no [discord](https://discordapp.com/developers/applications/), assim como tamb�m a cria��o de outro aplicativo no [Twitter](https://apps.twitter.com) foi necess�rio para realizar a integra��o com o mesmo. No caso do Twitter, ainda precisamos gerar nossos token de acesso (Access Token e Access Token Secret).

Depois disso, um terceiro aplicativo foi criado no [Heroku](https://dashboard.heroku.com/apps/) unicamente para colocarmos nosso bot 24h/dia online na nuvem. Dentro do Heroku, utilizamos vari�veis de ambiente para guardar as informa��es sens�veis de acesso. 

Ainda al�m dos aplicativos tamb�m criamos um projeto no [Google APIs](https://console.developers.google.com/apis/dashboard?), onde ativamos o Google Drive API e Google Sheets API, ainda geramos uma credencial do tipo "Chave da conta de servi�o" do tipo "JSON". Depois precisamos pegar o "client_email" dentro deste arquivo JSON e compartilharmos com ele a planilha que queremos ter acesso.

## M�dulo WhatsApp

O m�dulo do WhatsApp tem algumas limita��es conhecidas:
- Todas mencionadas no [WFAPI](https://github.com/SapoGitHub/Repositorio-Geral/tree/master/WFAPI);
- S� pode checar novas mensagens por comando;
- Problema quando reabrimos o bot e n�o foi removido a conex�o com o WhatsApp web anterior;
- Visualiza a conversa com o contato enquanto envia a mensagem para o mesmo.
- Esperar as repostas dos comandos antes de enviar um novo;
- N�o enviar muitas mensagens ao mesmo tempo. 
	- Alternativa: enviar uma mensagen grande ou com quebra de linha dentro de aspas.
	- Ex.:<code>!whats destinat�rio "Mensagem 1 \n Mensagem 2"</code>.
- Se desconecta depois de algum tempo de inatividade.

Melhorias poss�veis:
- Checar ultimas mensagens do contato antes de enviar nova;
- Agendar o envio de mensagens;
- Realizar a transcri��o de �udios;
- Realizar a convers�o de texto para �udio.

Recomenda��es:
- Enviar mensagens entre aspas (<code>!whats contato "mensagem completa"</code>);
- N�o estar recebendo novas mensagens enquanto checa novas mensagens na conversa.
