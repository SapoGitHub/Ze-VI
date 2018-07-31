# ZÉ VI

Para a criação do bot, foi necessário a criação de um aplicativo no [discord](https://discordapp.com/developers/applications/), assim como também a criação de outro aplicativo no [Twitter](https://apps.twitter.com) foi necessário para realizar a integração com o mesmo. No caso do Twitter, ainda precisamos gerar nossos token de acesso (Access Token e Access Token Secret).

Depois disso, um terceiro aplicativo foi criado no [Heroku](https://dashboard.heroku.com/apps/) unicamente para colocarmos nosso bot 24h/dia online na nuvem. Dentro do Heroku, utilizamos variáveis de ambiente para guardar as informações sensíveis de acesso. 

Ainda além dos aplicativos também criamos um projeto no [Google APIs](https://console.developers.google.com/apis/dashboard?), onde ativamos o Google Drive API e Google Sheets API, ainda geramos uma credencial do tipo "Chave da conta de serviço" do tipo "JSON". Depois precisamos pegar o "client_email" dentro deste arquivo JSON e compartilharmos com ele a planilha que queremos ter acesso.

Esse é um bot desenvolvido para meu pessoal, por isso alguns recursos se restringem a um máximo de 3 usuários específicos definidos no próprio código por exemplo, para ser utilizado em servidores maiores é necessário realizar as devidas adaptações.

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

Os comandos podem ser conferidos na [wiki](https://github.com/SapoGitHub/Ze-VI/wiki/Comandos).
