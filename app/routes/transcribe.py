from app.database import create_db_connection
from ..audio_processing import extract_audio_from_video
from app.utils import format_time
from app.whisper_model import model
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from datetime import datetime
import json
from app.crud import create_video, get_video_by_filename

router = APIRouter()

@router.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint para transcrição de vídeo ou áudio.
    Recebe um arquivo, verifica se já existe no banco, processa e salva a transcrição.
    Permite uso automático de GPU (CUDA) se disponível, senão CPU.
    """
    ext = os.path.splitext(file.filename)[1].lower()
    SUPPORTED_AUDIO = [".mp3", ".wav", ".m4a"]
    SUPPORTED_VIDEO = [".mp4", ".mov", ".mkv", ".webm", ".avi"]

    # Removido: detecção automática de GPU

    temp_video_path = None
    temp_audio_path = None
    try:
        # Verifica se o arquivo já está cadastrado no banco usando função do CRUD
        row = get_video_by_filename(file.filename)
        if row:
            try:
                dados = json.loads(row["dados"])
            except Exception:
                dados = row["dados"]
            return dados

        # Processa o arquivo se não estiver cadastrado
        temp_video_path = f"temp_{uuid.uuid4().hex}{ext}"
        contents = await file.read()
        with open(temp_video_path, "wb") as f:
            f.write(contents)

        # Extrai áudio se for vídeo
        if ext in SUPPORTED_VIDEO:
            temp_audio_path = extract_audio_from_video(temp_video_path)
        elif ext in SUPPORTED_AUDIO:
            temp_audio_path = temp_video_path
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")

        # ----- INÍCIO DO NOVO BLOCO DE CÓDIGO MOCKADO -----

        # Simula um resultado falso do Whisper AI
        mock_segments = [
            {"start": 0.5, "end": 2.8, "text": "Olá, este é o primeiro segmento da nossa transcrição de teste."},
            {"start": 3.0, "end": 5.5, "text": "Ela funciona de forma instantânea para agilizar o desenvolvimento."},
            {"start": 5.8, "end": 8.2, "text": "Obrigado por utilizar o modo de desenvolvimento mockado."}
        ]

        formatted_segments = mock_segments
        dados_json_str = json.dumps(formatted_segments, ensure_ascii=False)
        duration = 8.2
        full_text = "\n".join([seg['text'] for seg in formatted_segments])
        idioma = "pt"

        # ----- FIM DO NOVO BLOCO DE CÓDIGO MOCKADO -----

        # Salva no banco usando função do CRUD
        # Esta parte do código deve permanecer, utilizando as variáveis mockadas
        create_video(
            nome=os.path.splitext(file.filename)[0],
            dados=dados_json_str,
            nome_arquivo=file.filename,
            caminho_audio=temp_audio_path,
            caminho_txt=None,
            caminho_json=None,
            texto=full_text,
            idioma=idioma,
            duracao=duration
        )

        return formatted_segments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Remove arquivos temporários
        for path in [temp_audio_path, temp_video_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
