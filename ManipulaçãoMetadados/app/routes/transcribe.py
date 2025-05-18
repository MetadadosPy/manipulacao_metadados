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

router = APIRouter()  # <-- ESSA LINHA ESTAVA FALTANDO

# (restante do código continua como estava, incluindo @router.post...)

router = APIRouter() 
@router.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    SUPPORTED_AUDIO = [".mp3", ".wav", ".m4a"]
    SUPPORTED_VIDEO = [".mp4", ".mov", ".mkv", ".webm", ".avi"]

    temp_video_path = f"temp_{uuid.uuid4().hex}{ext}"
    temp_audio_path = None

    try:
        contents = await file.read()
        with open(temp_video_path, "wb") as f:
            f.write(contents)

        if ext in SUPPORTED_VIDEO:
            temp_audio_path = extract_audio_from_video(temp_video_path)
        elif ext in SUPPORTED_AUDIO:
            temp_audio_path = temp_video_path
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")

        result = model.transcribe(temp_audio_path, language="pt")

        formatted_segments = [
            {
                "start": format_time(segment['start']),
                "end": format_time(segment['end']),
                "text": segment['text'].strip()
            }
            for segment in result.get("segments", [])
        ]

        dados_json_str = json.dumps(formatted_segments, ensure_ascii=False)

        duration = round(result['segments'][-1]['end'] if result.get('segments') else 0, 2)

        connection = create_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO videos (
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
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        for path in [temp_audio_path, temp_video_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
