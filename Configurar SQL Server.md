Como configurar a Autenticação no SQL Server
Para que a sua equipe possa usar o usuário root e a senha 0000, você precisa habilitar a Autenticação do SQL Server e criar esse login. Por padrão, muitas instalações só permitem a Autenticação do Windows.

Habilitar a Autenticação do SQL Server:

No SSMS, clique com o botão direito do mouse no nome do seu servidor e selecione "Propriedades".

No menu lateral, vá em "Segurança".

Em "Autenticação do servidor", selecione a opção "Modo de Autenticação do SQL Server e do Windows".

Clique em OK e reinicie o serviço do SQL Server (no SQL Server Configuration Manager).

Criar o login root:

No SSMS, expanda a pasta "Segurança" e clique com o botão direito em "Logins".

Selecione "Novo Login...".

No campo "Nome de login", digite root.

Marque a opção "Autenticação do SQL Server".

Digite a senha 0000 nos campos "Senha" e "Confirmar senha". Desmarque a opção "Impor política de senha" para evitar problemas.

Vá para a página "Funções do Servidor" e marque a caixa sysadmin. Isso dará ao usuário root todos os privilégios.

Clique em OK para criar o login.

Com essas configurações, todos os participantes do seu projeto poderão se conectar ao SQL Server usando as credenciais que você definiu.
===============================

Criar o login root:

No SSMS, expanda a pasta "Segurança" e clique com o botão direito em "Logins".

Selecione "Novo Login...".

No campo "Nome de login", digite root.

Marque a opção "Autenticação do SQL Server".

Digite a senha 0000 nos campos "Senha" e "Confirmar senha". Desmarque a opção "Impor política de senha" para evitar problemas.

Vá para a página "Funções do Servidor" e marque a caixa sysadmin. Isso dará ao usuário root todos os privilégios.

Clique em OK para criar o login.

=====================
Solução: Navegando para a Instância Correta
A sua imagem mostra que você tem pelo menos duas configurações de rede: uma para "SQL Native Client" e outra para "SQL SERVER (MSSQLSERVER)".

No painel esquerdo, navegue até Configuração de Rede do SQL Server.

Clique no sinal de + (mais) para expandir a pasta "Protocolos para MSSQLSERVER".

No painel da direita, você verá a lista de protocolos (como Memória Compartilhada, TCP/IP e Pipes Nomeados).

Se o protocolo TCP/IP estiver desabilitado, clique com o botão direito e selecione Habilitar.

Depois de habilitar o TCP/IP, vá para Serviços do SQL Server no painel esquerdo.

Clique com o botão direito em "SQL Server (MSSQLSERVER)" e selecione Reiniciar.

Após reiniciar o serviço, tente se conectar novamente no SSMS.
=========================
Solução 🛠️
Para criar um novo banco de dados, você precisa se reconectar ao SQL Server com um usuário que tenha privilégios de administrador.

Desconecte-se do servidor no SSMS.

Na tela de login, mude a autenticação para Autenticação do Windows.

Clique em Conectar.

A Autenticação do Windows geralmente concede privilégios de administrador por padrão, a menos que as configurações de segurança tenham sido alteradas. Se a conexão for bem-sucedida, você poderá executar o comando CREATE DATABASE sem problemas.

Se você ainda quiser usar o usuário root que criamos, é provável que ele não tenha as permissões corretas. Para conceder as permissões:

Conecte-se com a Autenticação do Windows.

No painel "Object Explorer", expanda Segurança > Logons.

Clique com o botão direito no login root e selecione "Propriedades".

No menu esquerdo, vá para a página "Funções do Servidor" (Server Roles).

Marque a caixa de seleção para a função sysadmin.

Clique em OK.
===============================
2. Protocolo de Conexão TCP/IP Desabilitado
Mesmo com o nome do servidor correto, a conexão pode falhar se o protocolo de rede não estiver habilitado para a sua instância do SQL Server.

Para garantir que o protocolo está ativo, siga estes passos novamente:

Vá no menu Iniciar e procure por SQL Server Configuration Manager.

No painel esquerdo, vá em SQL Server Network Configuration e clique em Protocols for <sua-instancia> (por exemplo, Protocols for MSSQLSERVER ou Protocols for LEXUS).

No painel da direita, certifique-se de que o protocolo TCP/IP está Habilitado. Se não estiver, clique com o botão direito e habilite.

Vá em SQL Server Services, clique com o botão direito na sua instância do SQL Server e selecione Restart.
==================================
Serviço do SQL Server Parado (Mais Comum)
A causa mais frequente é que o serviço do SQL Server ou do Browser do SQL Server (se estiver usando instâncias nomeadas) não está em execução. Você consegue "encontrar" o servidor, mas ele não consegue processar seu login porque está parado.

🛠️ Ação:

Aperte Windows + R para abrir a caixa "Executar".

Digite services.msc e pressione Enter.

Na janela de Serviços, procure por:

SQL Server (MSSQLSERVER) se for a instância padrão.

SQL Server (NOME_DA_SUA_INSTANCIA) se for uma instância nomeada.

Certifique-se de que o Status do serviço esteja como "Em execução" (Running). Se não estiver, clique com o botão direito e selecione Iniciar.
====================================
Protocolos de Conexão Desabilitados
Como o erro menciona Shared Memory Provider, isso pode ser um problema com os protocolos que o SQL Server está usando ou permitindo.

🛠️ Ação:

Procure e abra o SQL Server Configuration Manager.

Expanda "Configuração de Rede do SQL Server".

Clique em "Protocolos para MSSQLSERVER" (ou o nome da sua instância).

Verifique se os protocolos Memória Compartilhada (Shared Memory), TCP/IP e Pipes Nomeados (Named Pipes) estão Habilitados (Enabled). Se algum estiver desabilitado, clique com o botão direito para habilitá-lo.

Importante: Se você fizer qualquer alteração aqui, você deve reiniciar o serviço do SQL Server (conforme explicado no Ponto 1) para que as mudanças entrem em vigor.
====================================
Abrir o Gerenciador de Serviços
Existem duas maneiras rápidas de fazer isso:

Método Rápido (Recomendado): Pressione as teclas Windows+R no seu teclado para abrir a caixa "Executar". Digite services.msc e pressione Enter.

1. Localizar o Serviço
Na janela de Serviços que se abrir, role a lista até encontrar o serviço do SQL Server. O nome dele geralmente é:

SQL Server (MSSQLSERVER): Se você estiver usando a instância padrão.

SQL Server (NOME_DA_SUA_INSTANCIA): Se você nomeou sua instância (substitua NOME_DA_SUA_INSTANCIA pelo nome que você usa, como SQLEXPRESS ou outro).
=================================
-botão direito - propriedades - segurança - modo de autenticação do sql server e do windows
-botão direito - propriedades - geral - nome (aqui esta o nome do banco para configurar)
-segurança - logon - botão direito - novo logon - geral
(autenticação sql - root - 0000)
-segurança - logon - botão direito - funções do servidor
(habilitar sysadmin)
-segurança - logon - botão direito - status
(conceder e habilitado)
windows + sql Server Configuration Manager
(Configuração de Rede do sql server - protocolos para MSSQLSERVER)
(Habilitar memoria/pipes/tcp/ip)
windows + r
services.msc
(procurar na lista SQL SERVER (MSSQLSERVER) ou outro e habilitar)
(clicar com botão direito e reiniciar)