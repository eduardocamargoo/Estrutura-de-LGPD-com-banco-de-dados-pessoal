import csv
import logging
import time
from functools import wraps
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, text
from datetime import datetime

logging.basicConfig(
    filename='atividades.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Iniciando execução da '{func.__name__}'...")
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        duracao = fim - inicio
        logging.info(f"Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

DB_USER = "alunos"
DB_PASS = "AlunoFatec"
DB_HOST = "174.138.65.214"
DB_PORT = "5432"
DB_NAME = "atividade2"

try:
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        echo=False
    )
    metadata = MetaData()
    usuarios = Table(
        'usuarios', metadata,
        Column('id', Integer, primary_key=True),
        Column('nome', String(50), nullable=False, index=True),
        Column('cpf', String(14), nullable=False),
        Column('email', String(100), nullable=False, unique=True),
        Column('telefone', String(20), nullable=False),
        Column('data_nascimento', Date, nullable=False),
        Column('created_on', DateTime(), default=datetime.now),
        Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
    )
    metadata.create_all(engine)

except Exception as e:
    logging.error(f"Erro ao conectar ou configurar o banco de dados: {e}")
    print(f"Erro de DB: {e}. Verifique as credenciais, VPN ou conexão com a internet.")
    exit()

def anonimizar_lgpd(row):
    try:
        dados = list(row)

        nome = dados[1]
        partes_nome = nome.split(' ', 1)
        primeiro_nome = partes_nome[0]
        resto_nome = f" {partes_nome[1]}" if len(partes_nome) > 1 else ""
        dados[1] = primeiro_nome[0] + ('*' * (len(primeiro_nome) - 1)) + resto_nome

        cpf = dados[2]
        if len(cpf) == 14:
            dados[2] = cpf[:3] + ".***.***-**"
        else:
            dados[2] = "***.***.***-**"

        email = dados[3]
        if '@' in email:
            local, domain = email.split('@', 1)
            dados[3] = local[0] + ('*' * (len(local) - 1)) + '@' + domain
        else:
            dados[3] = "**********"

        dados[4] = dados[4][-4:]

        return tuple(dados)
    except Exception as e:
        logging.warning(f"Erro ao anonimizar linha {row}: {e}")
        return row

@medir_tempo
def executar_atividade_2(todos_registros):
    logging.info("Iniciando Atividade 2: Exportação por ano (anonimizado).")
    dados_por_ano = {}
    
    for registro in todos_registros:
        registro_anonimizado = anonimizar_lgpd(registro) 
        data_nascimento = registro_anonimizado[5]
        
        if data_nascimento:
            ano = data_nascimento.year
            if ano not in dados_por_ano:
                dados_por_ano[ano] = []
            dados_por_ano[ano].append(registro_anonimizado)
        else:
            logging.warning(f"Registro {registro[0]} sem data de nascimento.")
            
    header = ['id', 'nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'created_on', 'updated_on']
    
    for ano, registros_do_ano in dados_por_ano.items():
        filename = f"{ano}.csv" 
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(registros_do_ano)
            logging.info(f"Arquivo '{filename}' criado com {len(registros_do_ano)} registros.")
        except IOError as e:
            logging.error(f"Erro ao escrever arquivo '{filename}': {e}")
            
    print(f"Atividade 2 concluída. {len(dados_por_ano)} arquivos de ano (CSV) criados.")
    logging.info(f"Atividade 2 concluída. {len(dados_por_ano)} arquivos de ano criados.")

@medir_tempo
def executar_atividade_3(todos_registros):
    logging.info("Iniciando Atividade 3: Exportação total (não-anonimizado).")
    filename = "todos.csv"
    header = ['nome', 'cpf']
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            
            for registro in todos_registros:
                nome = registro[1]
                cpf = registro[2]
                writer.writerow([nome, cpf])
                
        print(f"Atividade 3 concluída. Arquivo '{filename}' criado com {len(todos_registros)} registros.")
        logging.info(f"Atividade 3 concluída. Arquivo '{filename}' criado com {len(todos_registros)} registros.")
    except IOError as e:
        logging.error(f"Erro ao escrever arquivo '{filename}': {e}")

def main():
    logging.info("--- Iniciando processamento das atividades LGPD ---")
    print("Iniciando processamento... Verifique o 'atividades.log' para detalhes.")
    
    todos_os_registros = []
    try:
        with engine.connect() as conn:
            logging.info("Buscando todos os registros do banco de dados...")
            result = conn.execute(text("SELECT * FROM usuarios;"))
            todos_os_registros = result.fetchall()
        
        logging.info(f"Total de {len(todos_os_registros)} registros buscados do banco de dados.")
        print(f"{len(todos_os_registros)} registros encontrados. Executando atividades...")

    except Exception as e:
        logging.critical(f"Falha ao buscar dados do banco: {e}")
        print(f"Falha ao buscar dados do banco: {e}. Abortando.")
        return

    if not todos_os_registros:
        logging.warning("Nenhum registro encontrado no banco. Atividades 2 e 3 serão puladas.")
        print("Nenhum registro encontrado no banco.")
        return

    executar_atividade_2(todos_os_registros)
    executar_atividade_3(todos_os_registros)
    
    logging.info("--- Processamento finalizado ---")
    print("Processamento concluído.")

if __name__ == "__main__":
    main()