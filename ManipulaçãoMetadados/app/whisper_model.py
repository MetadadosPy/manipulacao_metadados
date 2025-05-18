import whisper

try:
    model = whisper.load_model("base")
except Exception as e:
    print(f"Falha ao carregar modelo Whisper: {str(e)}")
    raise
