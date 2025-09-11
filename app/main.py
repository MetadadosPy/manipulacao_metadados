from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import transcribe
from app.routes.videos import router as videos_router

# Inicialização da aplicação FastAPI
app = FastAPI()

# Configuração do middleware CORS
# Permite que o frontend acesse a API de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique seu front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão das rotas de transcrição e CRUD de vídeos
app.include_router(transcribe.router)  # Rotas para transcrição de vídeos/áudios
app.include_router(videos_router)      # Rotas CRUD para vídeos
