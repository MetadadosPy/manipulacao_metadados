from .database import create_db_connection
from .models import Video

# Função para listar todos os vídeos
def get_all_videos():
    """
    Retorna uma lista de todos os vídeos cadastrados no banco de dados.
    Cada vídeo é um dicionário com os campos da tabela 'videos'.
    """
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM videos')
    videos = cursor.fetchall()
    conn.close()
    return videos

# Função para criar um novo vídeo
def create_video(
    nome,
    dados,
    nome_arquivo,
    caminho_audio,
    caminho_txt,
    caminho_json,
    texto,
    idioma,
    duracao
):
    """
    Insere um novo vídeo transcrito no banco de dados.
    Parâmetros correspondem aos campos da tabela 'videos'.
    """
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO videos (nome, dados, nome_arquivo, caminho_audio, caminho_txt, caminho_json, texto, idioma, duracao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (nome, dados, nome_arquivo, caminho_audio, caminho_txt, caminho_json, texto, idioma, duracao)
    )
    conn.commit()
    conn.close()

# Função para atualizar um vídeo
def update_video(
    video_id,
    nome=None,
    dados=None,
    nome_arquivo=None,
    caminho_audio=None,
    caminho_txt=None,
    caminho_json=None,
    texto=None,
    idioma=None,
    duracao=None
):
    """
    Atualiza os campos de um vídeo existente no banco de dados.
    Só os campos informados serão atualizados.
    """
    conn = create_db_connection()
    cursor = conn.cursor()
    query = 'UPDATE videos SET '
    params = []
    updates = []
    if nome is not None:
        updates.append('nome=%s')
        params.append(nome)
    if dados is not None:
        updates.append('dados=%s')
        params.append(dados)
    if nome_arquivo is not None:
        updates.append('nome_arquivo=%s')
        params.append(nome_arquivo)
    if caminho_audio is not None:
        updates.append('caminho_audio=%s')
        params.append(caminho_audio)
    if caminho_txt is not None:
        updates.append('caminho_txt=%s')
        params.append(caminho_txt)
    if caminho_json is not None:
        updates.append('caminho_json=%s')
        params.append(caminho_json)
    if texto is not None:
        updates.append('texto=%s')
        params.append(texto)
    if idioma is not None:
        updates.append('idioma=%s')
        params.append(idioma)
    if duracao is not None:
        updates.append('duracao=%s')
        params.append(duracao)
    query += ', '.join(updates)
    query += ' WHERE id=%s'
    params.append(video_id)
    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

# Função para deletar um vídeo
def delete_video(video_id):
    """
    Remove um vídeo do banco de dados pelo seu ID.
    """
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM videos WHERE id=%s', (video_id,))
    conn.commit()
    conn.close()

# Função para buscar vídeo pelo nome do arquivo
def get_video_by_filename(nome_arquivo):
    """
    Busca um vídeo no banco de dados pelo nome do arquivo.
    Retorna o campo 'dados' se encontrado, ou None.
    """
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT dados FROM videos WHERE nome_arquivo = %s', (nome_arquivo,))
    row = cursor.fetchone()
    conn.close()
    return row
