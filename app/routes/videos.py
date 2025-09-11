from fastapi import APIRouter, HTTPException
from app.crud import get_all_videos, create_video, update_video, delete_video

router = APIRouter()

@router.get("/videos")
def list_videos():
    """
    Retorna uma lista de todos os vídeos cadastrados.
    Saída: lista de dicionários com os campos da tabela 'videos'.
    """
    return get_all_videos()

@router.post("/videos")
def add_video(video: dict):
    """
    Cria um novo vídeo no banco de dados.
    Parâmetro: video (dict) - dados do vídeo conforme modelo.
    Saída: mensagem de sucesso ou erro.
    """
    try:
        create_video(
            video.get("nome"),
            video.get("dados"),
            video.get("nome_arquivo"),
            video.get("caminho_audio"),
            video.get("caminho_txt"),
            video.get("caminho_json"),
            video.get("texto"),
            video.get("idioma"),
            video.get("duracao")
        )
        return {"message": "Vídeo criado com sucesso"}
    except Exception as e:
        # Retorna erro HTTP 500 em caso de falha
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/videos/{video_id}")
def edit_video(video_id: int, video: dict):
    """
    Atualiza os dados de um vídeo existente.
    Parâmetros: video_id (int), video (dict) - dados a atualizar.
    Saída: mensagem de sucesso ou erro.
    """
    try:
        update_video(
            video_id,
            video.get("nome"),
            video.get("dados"),
            video.get("nome_arquivo"),
            video.get("caminho_audio"),
            video.get("caminho_txt"),
            video.get("caminho_json"),
            video.get("texto"),
            video.get("idioma"),
            video.get("duracao")
        )
        return {"message": "Vídeo atualizado com sucesso"}
    except Exception as e:
        # Retorna erro HTTP 500 em caso de falha
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/videos/{video_id}")
def remove_video(video_id: int):
    """
    Remove um vídeo do banco de dados pelo ID.
    Parâmetro: video_id (int).
    Saída: mensagem de sucesso ou erro.
    """
    try:
        delete_video(video_id)
        return {"message": "Vídeo deletado com sucesso"}
    except Exception as e:
        # Retorna erro HTTP 500 em caso de falha
        raise HTTPException(status_code=500, detail=str(e))
