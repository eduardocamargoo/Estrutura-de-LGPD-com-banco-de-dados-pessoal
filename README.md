Projeto de Anonimização de Dados (LGPD) - Fatec Rio Claro
Script Python desenvolvido como "Segundo Mini Projeto" da Fatec Rio Claro , focado na aplicação prática de conceitos da Lei Geral de Proteção de Dados (LGPD).



Este projeto conecta-se a um banco de dados PostgreSQL, processa registros de usuários e aplica regras de anonimização de dados antes de exportá-los para arquivos CSV. O objetivo é demonstrar a manipulação segura de dados pessoais, conforme exigido pela LGPD (Lei nº 13.709/2018).


📝 Descrição das Atividades
O script implementa quatro atividades principais conforme especificado no documento da atividade:

Atividade 1: Função de Anonimização
O núcleo do projeto é uma função que anonimiza dados pessoais. As seguintes regras são aplicadas:

Nome: Substitui as letras do primeiro nome por *, exceto a primeira.

Exemplo: Olivia Araújo → O***** Araújo 

CPF: Substitui os últimos 8 dígitos por *.

Exemplo: 237.615.809-59 → 237.***.***-** 


E-mail: Substitui os caracteres do nome de usuário por *, exceto o primeiro.

Exemplo: nuneserick@example.com → n*********@example.com 


Telefone: Apresenta apenas os 4 últimos dígitos.

Exemplo: +55 (011) 9483-6810 → 6810 


Atividade 2: Exportação por Ano (Anonimizado)
O script processa todos os registros do banco de dados e os agrupa por ano de nascimento.

Gera arquivos .csv separados para cada ano (ex: 1990.csv, 1991.csv, etc.).

Todos os dados contidos nesses arquivos são anonimizados conforme as regras da Atividade 1.

Atividade 3: Exportação Total (Não-Anonimizado)
O script gera um arquivo único chamado todos.csv.

Este arquivo contém apenas as colunas nome e cpf de todos os usuários.

Os dados neste arquivo não devem ser anonimizados.

Atividade 4: Monitoramento e Logging
O tempo de execução das Atividades 2 e 3 é mensurado usando um decorator Python.

O decorator medir_tempo foi adaptado para gravar os tempos de início, fim e duração de cada atividade em um arquivo de log chamado atividades.log.

 Tecnologias e Dependências
Este projeto utiliza Python 3 e se conecta a um banco de dados PostgreSQL. As principais bibliotecas estão listadas no arquivo requirements.txt:

Faker==37.11.0
greenlet==3.2.4
psycopg2-binary==2.9.10
SQLAlchemy==2.0.43
typing_extensions==4.15.0
tzdata==2025.2

SQLAlchemy: Usada para a conexão com o banco (ORM) e definição do modelo de dados.


psycopg2-binary: Driver Python para PostgreSQL.

csv (biblioteca nativa): Usada para gerar os arquivos .csv.

logging (biblioteca nativa): Usada para registrar os tempos de execução.

Como Executar
Clone este repositório:

Bash

git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
Instale as dependências:

Bash

pip install -r requirements.txt
O script está pré-configurado para se conectar ao banco de dados da atividade :

Host: xxx.xxx.xxx-xx

Database: atividade2

User: alunos

Password: AlunoFatec

Execute o script principal:

Bash

python solucao_lgpd.py
 Saída (Resultados)
Após a execução, os seguintes arquivos serão gerados no diretório raiz:

atividades.log: Um arquivo de log detalhando o início, fim e tempo de execução das Atividades 2 e 3.

[ANO].csv (ex: 1990.csv, 1991.csv...): Múltiplos arquivos CSV, um para cada ano de nascimento encontrado, contendo os dados anonimizados dos usuários.

todos.csv: Um arquivo CSV único contendo apenas o nome e cpf originais (não anonimizados) de todos os usuários.
