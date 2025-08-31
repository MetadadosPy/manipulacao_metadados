"""
transcribe.py
-------------
Define as rotas relacionadas à transcrição de áudio usando o modelo Whisper.

Este módulo expõe a rota principal `/transcribe/` para upload de arquivos de áudio ou vídeo, realiza a transcrição usando o modelo Whisper,
formata os resultados, armazena no banco de dados e retorna os segmentos transcritos.

Boas práticas:
- Docstrings de módulo, funções e rotas.
- Organização clara das dependências e respostas.
- Tratamento robusto de erros e limpeza de arquivos temporários.

Dependências:
- FastAPI, Whisper, ffmpeg, MySQL Connector, utilitários do projeto.
"""

from ..audio_processing import extract_audio_from_video
from app.database import create_db_connection
from app.utils import format_time
from app.whisper_model import model
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import whisper
import os
import uuid
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import json
import traceback


router = APIRouter()

# (restante do código continua como estava, incluindo @router.post...)

router = APIRouter() 
@router.post("/transcribe/", response_model=list)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Recebe um arquivo de áudio ou vídeo, realiza a transcrição usando Whisper e armazena os resultados no banco de dados.

    Args:
        file (UploadFile): Arquivo de áudio (.mp3, .wav, .m4a) ou vídeo (.mp4, .mov, .mkv, .webm, .avi) enviado pelo usuário.

    Returns:
        list: Lista de segmentos transcritos, cada um contendo início, fim e texto.

    Raises:
        HTTPException: Para erros de formato de arquivo, processamento ou banco de dados.
    """

    # Extensão do arquivo recebido
    ext = os.path.splitext(file.filename)[1].lower()
    SUPPORTED_AUDIO = [".mp3", ".wav", ".m4a"]
    SUPPORTED_VIDEO = [".mp4", ".mov", ".mkv", ".webm", ".avi"]

    # Caminhos temporários para processamento
    temp_video_path = f"temp_{uuid.uuid4().hex}{ext}"
    temp_audio_path = None

    try:
        # Salva o arquivo recebido em disco temporariamente
        contents = await file.read()
        with open(temp_video_path, "wb") as f:
            f.write(contents)

        # Se for vídeo, extrai o áudio; se for áudio, usa diretamente
        if ext in SUPPORTED_VIDEO:
            temp_audio_path = extract_audio_from_video(temp_video_path)
        elif ext in SUPPORTED_AUDIO:
            temp_audio_path = temp_video_path
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")

        # Transcreve o áudio usando Whisper
        result = model.transcribe(temp_audio_path, language="pt")

        # Formata os segmentos para resposta e armazenamento
        formatted_segments = [
            {
                "start": float(segment['start']),
                "end": float(segment['end']),
                "text": segment['text'].strip()
            }
            for segment in result.get("segments", [])
        ]

        # Serializa os dados para o banco
        dados_json_str = json.dumps(formatted_segments, ensure_ascii=False)

        # Duração total do áudio
        duration = round(result['segments'][-1]['end'] if result.get('segments') else 0, 2)

        # Salva no banco de dados
        connection = create_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT IGNORE INTO videos (
                nome, dados, nome_arquivo, caminho_audio, 
                texto, idioma, duracao
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        full_text = "\n".join([seg['text'] for seg in formatted_segments])

        values = (
            os.path.splitext(file.filename)[0],
            dados_json_str,
            file.filename,
            temp_audio_path,
            full_text,
            result.get("language", "unknown"),
            duration
        )

        cursor.execute(query, values)
        connection.commit()

        return formatted_segments

    except Exception as e:
        # Retorna erro detalhado para o cliente
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Limpa arquivos temporários e fecha conexão
        for path in [temp_audio_path, temp_video_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
