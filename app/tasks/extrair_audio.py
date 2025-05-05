import ffmpeg         # Importa a biblioteca ffmpeg-python para manipulação de áudio e vídeo
import tempfile       # Usado para criar arquivos temporários
import os             # Módulo para interações com o sistema operacional

def extract_audio_from_video(video_path: str, audio_format: str = "mp3") -> str:
    # Define o caminho absoluto do executável ffmpeg
    # IMPORTANTE: este caminho precisa existir no PC onde o script for executado
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Altere se necessário
    # Cria um arquivo temporário com extensão de áudio (ex: .mp3) onde o áudio será salvo
    temp_audio_path = tempfile.mktemp(suffix=f".{audio_format}")
    try:
        # Executa o comando FFmpeg para extrair o áudio do vídeo
        # .input() define o arquivo de entrada (vídeo)
        # .output() define o arquivo de saída (áudio)
        # .run() executa o comando e passa o caminho personalizado para o ffmpeg.exe
        ffmpeg.input(video_path).output(temp_audio_path).run(cmd=ffmpeg_path) 
        # Retorna o caminho do arquivo de áudio gerado
        return temp_audio_path
    except Exception as e:
        # Em caso de erro, lança uma exceção com uma mensagem explicativa
        raise Exception(f"Erro ao extrair áudio do vídeo: {str(e)}")

# ========== Exemplo de uso ==========
# Define o caminho do vídeo de onde o áudio será extraído
video_path = "video.mp4"  # Substitua pelo nome/caminho do vídeo real
# Chama a função e salva o caminho do áudio extraído
audio_path = extract_audio_from_video(video_path)
# Exibe o caminho onde o áudio foi salvo
print(f"Áudio extraído para: {audio_path}")
