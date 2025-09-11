class Video:
    """
    Modelo que representa um vídeo transcrito no sistema.
    Cada instância corresponde a um registro na tabela 'videos' do banco de dados.

    Atributos:
        id (int): Identificador único do vídeo.
        nome (str): Nome do vídeo.
        dados (str): Transcrição segmentada em JSON.
        nome_arquivo (str): Nome do arquivo de vídeo.
        caminho_audio (str): Caminho do arquivo de áudio extraído.
        caminho_txt (str): Caminho do arquivo TXT gerado (opcional).
        caminho_json (str): Caminho do arquivo JSON gerado (opcional).
        texto (str): Transcrição completa em texto.
        idioma (str): Idioma detectado da transcrição.
        duracao (float): Duração do vídeo em segundos.
        data_transcricao (datetime): Data/hora da transcrição.
    """
    def __init__(self, id, nome, dados, nome_arquivo, caminho_audio, caminho_txt, caminho_json, texto, idioma, duracao, data_transcricao):
        self.id = id  # Identificador único
        self.nome = nome  # Nome do vídeo
        self.dados = dados  # Transcrição segmentada (JSON)
        self.nome_arquivo = nome_arquivo  # Nome do arquivo de vídeo
        self.caminho_audio = caminho_audio  # Caminho do áudio extraído
        self.caminho_txt = caminho_txt  # Caminho do TXT (opcional)
        self.caminho_json = caminho_json  # Caminho do JSON (opcional)
        self.texto = texto  # Transcrição completa
        self.idioma = idioma  # Idioma detectado
        self.duracao = duracao  # Duração em segundos
        self.data_transcricao = data_transcricao  # Data/hora da transcrição
