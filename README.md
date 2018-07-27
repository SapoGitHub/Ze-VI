# Zé VI


Para a criação do bot, foi necessário a criação de um aplicativo no [discord](https://discordapp.com/developers/applications/), assim como também a criação de outro aplicativo no [Twitter](https://apps.twitter.com) foi necessário para realizar a integração com o mesmo. No caso do Twitter, ainda precisamos gerar nossos token de acesso (Access Token e Access Token Secret).

Depois disso, um terceiro aplicativo foi criado no [Heroku](https://dashboard.heroku.com/apps/) unicamente para colocarmos nosso bot 24h/dia online na nuvem. Dentro do Heroku, utilizamos variáveis de ambiente para guardar as informações sensíveis de acesso. 

Ainda além dos aplicativos também criamos um projeto no [Google APIs](https://console.developers.google.com/apis/dashboard?), onde ativamos o Google Drive API e Google Sheets API, ainda geramos uma credencial do tipo "Chave da conta de serviço" do tipo "JSON". Depois precisamos pegar o "client_email" dentro deste arquivo JSON e compartilharmos com ele a planilha que queremos ter acesso.

## Módulo WhatsApp

O módulo do WhatsApp tem algumas limitações conhecidas:
- Todas mencionadas no [WFAPI](https://github.com/SapoGitHub/Repositorio-Geral/tree/master/WFAPI);
- Só pode checar novas mensagens por comando;
- Prefência enviar mensagens entre aspas (<code>!whats contato "mensagem completa"</code>);
- Problema quando reabrimos o bot e não foi removido a conexão com o WhatsApp web anterior;
- Nenhuma função pode levar mais de 1 minuto ou o Discsord dá erro;
- Visualiza a conversa com o contato enquanto envia a mensagem para o mesmo.
- Recomendado não estar recebendo novas mensagens enquanto checa novas mensagens na conversa;
- Esperar as repostas dos comandos antes de enviar um novo.