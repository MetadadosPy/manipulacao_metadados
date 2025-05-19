# API de Transcrição de Áudio/Vídeo

Esta API permite o upload de arquivos de áudio ou vídeo para transcrição automática utilizando o modelo Whisper. Os dados transcritos são armazenados em um banco de dados MySQL.

## Requisitos

- Python 3.11+
- MySQL
- ffmpeg instalado no sistema

Instale as dependências com:

```sh
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

## Como Rodar
Execute o servidor com:
```
uvicorn app.main:app --reload
```
## Endpoints
POST /transcribe/
Faz upload de um arquivo de áudio ou vídeo e retorna a transcrição segmentada.

## Payload
Envie um arquivo usando multipart/form-data no campo file.

## Exemplo usando curl:
```
curl -X POST "http://localhost:8000/transcribe/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/para/seu_arquivo.mp4"
```
file: Arquivo de áudio (.mp3, .wav, .m4a) ou vídeo (.mp4, .mov, .mkv, .webm, .avi).

## Resposta
```
[
  {
    "start": "00:00",
    "end": "00:10",
    "text": "Texto transcrito do segmento"
  },
  ...
]
```
## Observações
- Os arquivos enviados são processados e removidos após a transcrição.
- Os dados completos são salvos na tabela videos do banco de dados configurado em app/config.py.
- Para alterar o idioma da transcrição, ajuste o parâmetro language no método model.transcribe em app/routes/transcribe.py.
---
Feito com FastAPI e OpenAI Whisper.


