import pandas as pd
import sqlite3

def load_segment_translation():
    translation_df = pd.read_excel('segmentos_unicos.xlsx')
    pt_to_en = translation_df.set_index('Segment Portuguese')['Segment'].to_dict()
    en_to_pt = translation_df.set_index('Segment')['Segment Portuguese'].to_dict()
    return pt_to_en, en_to_pt

# Conectar ao banco de dados SQLite
def connect_db():
    return sqlite3.connect('empresas_db.sqlite')

def query_db(query):
    conn = connect_db()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def filter_db(query, param):
    conn = connect_db()
    df = pd.read_sql(query, conn, params=(param,))
    conn.close()
    return df

# Função para carregar dados das empresas
def load_empresas():
    return query_db('SELECT "Nome Empresa", "Endereço da Empresa", Website, "Nome Contato", "Cargo Contato", "Telefone", LATITUDE, LONGITUDE FROM Empresas')

def load_segmentos(pt_to_en):
    # Certifique-se de que a consulta SQL esteja correta e alinhada com os nomes das colunas no seu banco de dados
    df = query_db('SELECT DISTINCT "Segmento" FROM SegmentoEmpresa')
    # Traduz os segmentos para inglês usando o dicionário pt_to_en
    segments_in_english = [pt_to_en.get(segmento_pt, segmento_pt) for segmento_pt in df['Segmento']]
    return segments_in_english

# Função para carregar produtos únicos

def load_produtos():
    query = """
    SELECT DISTINCT Produtos."Produto Ingles"
    FROM Produtos
    JOIN EmpresaProduto ON Produtos.Produto = EmpresaProduto.Produto
    """
    df = query_db(query)
    return df['Produto Ingles'].tolist()

def load_estados():
    query = "SELECT DISTINCT Estado FROM Empresas ORDER BY Estado"
    df = query_db(query)
    return df['Estado'].tolist()

# Função para filtrar empresas por segmento

def filter_by_segmento(segmento):
    query = """
    SELECT Empresas."Nome Empresa", Empresas."Endereço da Empresa", Empresas.Website, Empresas."Nome Contato", Empresas."Cargo Contato", Empresas."Telefone", Empresas.LATITUDE, Empresas.LONGITUDE
    FROM Empresas
    JOIN SegmentoEmpresa ON Empresas."Nome Empresa" = SegmentoEmpresa."Nome Empresa"
    WHERE SegmentoEmpresa.Segmento = ?
    """
    return filter_db(query, segmento)

# Função para filtrar empresas por produto

def filter_by_produto(produto):
    query = """
    SELECT DISTINCT Empresas."Nome Empresa", Empresas."Endereço da Empresa", Empresas.Website, Empresas."Nome Contato", Empresas."Cargo Contato", Empresas."Telefone", Empresas.LATITUDE, Empresas.LONGITUDE
    FROM Empresas
    JOIN EmpresaProduto ON Empresas."Nome Empresa" = EmpresaProduto."Nome Empresa"
    JOIN Produtos ON EmpresaProduto.Produto = Produtos.Produto
    WHERE Produtos."Produto Ingles" = ?
    """
    return filter_db(query, produto)

def filter_by_estado(estado):
    query = """
    SELECT "Nome Empresa", "Endereço da Empresa", Website, "Nome Contato", "Cargo Contato", "Telefone", LATITUDE, LONGITUDE
    FROM Empresas
    WHERE Estado = ?
    """
    return filter_db(query, estado)
