from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import clients, webhooks

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("🚀 API inicializada com sucesso")

    yield

    logger.info("🛑 API finalizada")

app = FastAPI(
    title="Mundo Invest API",
    version="1.0.0",
    description="Sistema de gestão de clientes e integração simulada com Pipefy",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "ok",
        "service": "Mundo Invest API",
        "version": "1.0.0",
    }

app.include_router(clients.router)
app.include_router(webhooks.router)