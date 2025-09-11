"""
Módulo responsável por carregar o modelo Whisper para transcrição automática.
O modelo é utilizado em todo o backend para processar áudios e vídeos.
"""

import whisper

try:
    # Carrega o modelo Whisper (base) exclusivamente na GPU (CUDA)
    model = whisper.load_model("base", device="cuda")
except Exception as e:
    print(f"Falha ao carregar modelo Whisper: {str(e)}")
    raise
