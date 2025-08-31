"""
whisper_model.py
-----------------
Módulo responsável por carregar o modelo Whisper para transcrição de áudio.
Agora configurado para rodar obrigatoriamente em CPU.

Boas práticas:
- Utiliza docstrings para documentação.
- Facilita manutenção e entendimento do código.
"""

import whisper

def get_whisper_model(model_name: str = "base") -> whisper.Whisper:
    """
    Carrega o modelo Whisper na CPU.

    Args:
        model_name (str): Nome do modelo Whisper a ser carregado (ex: "base", "small", "medium", "large").

    Returns:
        whisper.Whisper: Instância do modelo Whisper carregado na CPU.
    """
    return whisper.load_model(model_name, device="cpu")

# Instância global do modelo Whisper carregado na CPU
model = get_whisper_model("base")
    
