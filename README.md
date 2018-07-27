# Z� VI


Para a cria��o do bot, foi necess�rio a cria��o de um aplicativo no [discord](https://discordapp.com/developers/applications/), assim como tamb�m a cria��o de outro aplicativo no [Twitter](https://apps.twitter.com) foi necess�rio para realizar a integra��o com o mesmo. No caso do Twitter, ainda precisamos gerar nossos token de acesso (Access Token e Access Token Secret).

Depois disso, um terceiro aplicativo foi criado no [Heroku](https://dashboard.heroku.com/apps/) unicamente para colocarmos nosso bot 24h/dia online na nuvem. Dentro do Heroku, utilizamos vari�veis de ambiente para guardar as informa��es sens�veis de acesso. 

Ainda al�m dos aplicativos tamb�m criamos um projeto no [Google APIs](https://console.developers.google.com/apis/dashboard?), onde ativamos o Google Drive API e Google Sheets API, ainda geramos uma credencial do tipo "Chave da conta de servi�o" do tipo "JSON". Depois precisamos pegar o "client_email" dentro deste arquivo JSON e compartilharmos com ele a planilha que queremos ter acesso.

## M�dulo WhatsApp

O m�dulo do WhatsApp tem algumas limita��es conhecidas:
- Todas mencionadas no [WFAPI](https://github.com/SapoGitHub/Repositorio-Geral/tree/master/WFAPI);
- S� pode checar novas mensagens por comando;
- Pref�ncia enviar mensagens entre aspas (<code>!whats contato "mensagem completa"</code>);
- Problema quando reabrimos o bot e n�o foi removido a conex�o com o WhatsApp web anterior;
- Nenhuma fun��o pode levar mais de 1 minuto ou o Discsord d� erro;
- Visualiza a conversa com o contato enquanto envia a mensagem para o mesmo.
- Recomendado n�o estar recebendo novas mensagens enquanto checa novas mensagens na conversa;
- Esperar as repostas dos comandos antes de enviar um novo.