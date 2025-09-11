"""
Funções utilitárias para o projeto de manipulação de metadados.
Inclui conversão de tempo e outras funções auxiliares.
"""

def format_time(seconds):
    """
    Converte um valor em segundos para o formato mm:ss.
    Útil para exibir duração de áudios ou vídeos.

    Parâmetros:
        seconds (float/int): Tempo em segundos.
    Retorno:
        str: Tempo formatado como mm:ss.
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
