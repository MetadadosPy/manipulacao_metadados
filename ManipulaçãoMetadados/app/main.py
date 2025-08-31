"""
main.py
-------
Ponto de entrada da aplicação FastAPI para manipulação de metadados e transcrição de áudio.

Este módulo inicializa a aplicação FastAPI, configura o CORS e inclui as rotas de transcrição.

Boas práticas:
- Docstrings de módulo e funções.
- Organização clara dos imports e inicialização da aplicação.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transcribe

def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI, incluindo middlewares e rotas.

    Returns:
        FastAPI: Instância da aplicação configurada.
    """
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ou especifique seu front-end
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(transcribe.router)
    return app

app = create_app()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transcribe

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique seu front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transcribe.router)
