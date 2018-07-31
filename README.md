# ZÉ VI

Para a criação do bot, foi necessário a criação de um aplicativo no [discord](https://discordapp.com/developers/applications/), assim como também a criação de outro aplicativo no [Twitter](https://apps.twitter.com) foi necessário para realizar a integração com o mesmo. No caso do Twitter, ainda precisamos gerar nossos token de acesso (Access Token e Access Token Secret).

Depois disso, um terceiro aplicativo foi criado no [Heroku](https://dashboard.heroku.com/apps/) unicamente para colocarmos nosso bot 24h/dia online na nuvem. Dentro do Heroku, utilizamos variáveis de ambiente para guardar as informações sensíveis de acesso. 

Ainda além dos aplicativos também criamos um projeto no [Google APIs](https://console.developers.google.com/apis/dashboard?), onde ativamos o Google Drive API e Google Sheets API, ainda geramos uma credencial do tipo "Chave da conta de serviço" do tipo "JSON". Depois precisamos pegar o "client_email" dentro deste arquivo JSON e compartilharmos com ele a planilha que queremos ter acesso.

Esse é um bot desenvolvido para meu pessoal, por isso alguns recursos se restringem a um máximo de 3 usuários específicos definidos no próprio código por exemplo, para ser utilizado em servidores maiores é necessário realizar as devidas adaptações.

Informações mais completas sobre melhorias futuras, limitações e os comandos podem ser conferidas na [wiki](https://github.com/SapoGitHub/Ze-VI/wiki).
