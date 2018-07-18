# Zé VI


Para a criação do bot, foi necessário a criação de um aplicativo no [discord](https://discordapp.com/developers/applications/), assim como também a criação de outro aplicativo no [Twitter](https://apps.twitter.com) foi necessário para realizar a integração com o mesmo. No caso do Twitter, ainda precisamos gerar nossos token de acesso (Access Token e Access Token Secret)

Depois disso, um terceiro aplicativo foi criado no [Heroku](https://dashboard.heroku.com/apps/) unicamente para colocarmos nosso bot 24h/dia online na nuvem. Dentro do Heroku, utilizamos variáveis de ambiente para guardar as informações vitais de acesso. 


Ainda além dos aplicativos também criamos um projeto no [Google APIs](https://console.developers.google.com/apis/dashboard?), onde ativamos o Google Drive API e geramos uma credencial do tipo "Chave da conta de serviço" do tipo "JSON". Depois precisamos pegar o "client_email" dentro deste arquivo JSON e compartilharmos com ele a planilha que queremos ter acesso.