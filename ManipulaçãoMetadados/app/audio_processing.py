import ffmpeg
import tempfile
import subprocess
import json

ALIAS_FORMATOS = {
    "matroska": "mkv",
    "mov": "mov",
    "mp4": "mp4",
    "webm": "webm",
    "avi": "avi"
}

FORMATOS_SUPORTADOS = {"mp4", "mov", "mkv", "webm", "avi"}


def get_format_from_video(video_path: str) -> str:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=format_name",
                "-of", "json",
                video_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            raise Exception(result.stderr.strip())

        format_info = json.loads(result.stdout)
        raw_format = format_info["format"]["format_name"]
        detected_formats = raw_format.lower().split(",")

        for f in detected_formats:
            if f in ALIAS_FORMATOS:
                return ALIAS_FORMATOS[f]
        return detected_formats[0]

    except Exception as e:
        raise Exception(f"Erro ao identificar o formato do vídeo: {str(e)}")


def extract_audio_from_video(video_path: str, audio_format: str = "mp3") -> str:
    video_format = get_format_from_video(video_path)
    print(f"Formato detectado: {video_format}")

    if video_format.lower() not in FORMATOS_SUPORTADOS:
        raise Exception(f"Formato '{video_format}' não é suportado. "
                        f"Formatos permitidos: {', '.join(FORMATOS_SUPORTADOS)}")

    temp_audio_path = tempfile.mktemp(suffix=f".{audio_format}")

    try:
        (
            ffmpeg
            .input(video_path)
            .output(
                temp_audio_path,
                format="mp3",
                acodec="libmp3lame",
                audio_bitrate="128k",
                threads=0,
                preset="ultrafast",
                ac=1,
                ar="16000"
            )
            .overwrite_output()
            .run(quiet=True)
        )
        return temp_audio_path

    except Exception as e:
        raise Exception(f"Erro ao extrair áudio do vídeo: {str(e)}")
