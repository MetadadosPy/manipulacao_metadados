"""
utils.py
--------
Funções utilitárias para formatação e manipulação de dados auxiliares.

Boas práticas:
- Docstrings de módulo e funções.
- Funções simples e reutilizáveis.
"""

def format_time(seconds):
    """Converte segundos para formato mm:ss"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
