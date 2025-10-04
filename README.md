pip install flask sqlalchemy sqlalchemy-utils pyodbc

Configurar SQL Server:

-botão direito - propriedades - segurança - modo de autenticação do sql server e do windows
-botão direito - propriedades - geral - nome (aqui esta o nome do banco para configurar)
-segurança - logon - botão direito - novo logon - geral
(autenticação sql - root - 0000)
-segurança - logon - botão direito - funções do servidor
(habilitar sysadmin)
-segurança - logon - botão direito - status
(conceder e habilitado)
-windows + sql Server Configuration Manager
(Configuração de Rede do sql server - protocolos para MSSQLSERVER)
(Habilitar memoria/pipes/tcp/ip)
-windows + r
services.msc
(procurar na lista SQL SERVER (MSSQLSERVER) ou outro e habilitar)
(clicar com botão direito e reiniciar)