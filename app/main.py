from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import clients, webhooks


# ----------------------
# LOGGER CONFIG
# ----------------------
logger = logging.getLogger("uvicorn")


# ----------------------
# LIFESPAN (ciclo de vida moderno)
# ----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    Base.metadata.create_all(bind=engine)
    logger.info("🚀 API inicializada com sucesso")

    yield

    # SHUTDOWN
    logger.info("🛑 API finalizada")


# ----------------------
# APP INIT
# ----------------------
app = FastAPI(
    title="Mundo Invest API",
    version="1.0.0",
    description="Sistema de gestão de clientes e integração simulada com Pipefy",
    lifespan=lifespan,
)


# ----------------------
# CORS
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: restringir domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------
# HEALTH CHECK
# ----------------------
@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "ok",
        "service": "Mundo Invest API",
        "version": "1.0.0",
    }


# ----------------------
# ROUTES
# ----------------------
app.include_router(clients.router)
app.include_router(webhooks.router)