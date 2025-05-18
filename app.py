from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import whisper
import os
import uuid
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import json
import traceback

app = FastAPI()

# Carrega o modelo uma vez ao iniciar
try:
    model = whisper.load_model("base")
except Exception as e:
    print(f"Falha ao carregar modelo Whisper: {str(e)}")
    raise

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'database': 'meta_dados_band',
    'user': 'root',
    'password': 'password'
}


def format_time(seconds):
    """Converte segundos para formato mm:ss"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def create_db_connection():
    """Cria e retorna uma conexão com o banco de dados"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        error_msg = f"Erro ao conectar ao MySQL: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".mp3", ".wav", ".m4a", ".webm", ".mp4"]:
        raise HTTPException(status_code=400, detail="Formato de áudio não suportado.")

    temp_filename = f"temp_{uuid.uuid4().hex}{ext}"

    try:
        # Salva arquivo temporariamente
        contents = await file.read()
        with open(temp_filename, "wb") as f:
            f.write(contents)

        if not os.path.exists(temp_filename):
            raise HTTPException(status_code=500, detail="Falha ao salvar arquivo temporário")

        try:
            result = model.transcribe(temp_filename, language="en")
        except Exception as e:
            error_msg = f"Falha na transcrição: {str(e)}"
            print(f"Erro Whisper: {error_msg}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=error_msg)

        # Formata os segmentos no formato desejado
        try:
            formatted_segments = [
                {
                    "start": format_time(segment['start']),
                    "end": format_time(segment['end']),
                    "text": segment['text'].strip()
                }
                for segment in result.get("segments", [])
            ]

            dados_json_str = json.dumps(formatted_segments, ensure_ascii=False)
        except Exception as e:
            error_msg = f"Erro ao formatar JSON: {str(e)}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

        # Calcula duração total
        try:
            duration = round(result['segments'][-1]['end'] if result.get('segments') else 0, 2)
        except Exception as e:
            duration = 0
            print(f"Erro ao calcular duração: {str(e)}")

        # Conexão com o banco de dados
        try:
            connection = create_db_connection()
            cursor = connection.cursor()

            query = """
            INSERT INTO videos (
                nome, dados, nome_arquivo, caminho_audio, 
                texto, idioma, duracao
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # Junta todos os textos para o campo 'texto' no banco
            full_text = "\n".join([seg['text'] for seg in formatted_segments])

            values = (
                os.path.splitext(file.filename)[0],
                dados_json_str,
                file.filename,
                temp_filename,
                full_text,
                result.get("language", "unknown"),
                duration
            )

            cursor.execute(query, values)
            connection.commit()
            video_id = cursor.lastrowid

        except Error as e:
            error_msg = f"Erro no banco de dados: {str(e)}"
            print(f"Erro MySQL: {error_msg}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=error_msg)
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

        # Remove arquivo temporário
        try:
            os.remove(temp_filename)
        except Exception as e:
            print(f"AVISO: Não foi possível remover arquivo temporário: {str(e)}")

        return formatted_segments  # Retorna diretamente o array formatado

    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Erro inesperado: {str(e)}"
        print(f"Erro completo:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)
    finally:
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)