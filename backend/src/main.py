import faiss
import fasttext
import compress_fasttext
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from .query_steam import router as steam_api_router
from .auth import router as auth_router
from .query_ml_model import router as ml_router, models

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading AI resources...")
    
    src_folder = os.path.dirname(os.path.abspath(__file__))
    root_folder = os.path.dirname(src_folder)
    data_folder = os.path.join(root_folder, "data")

    models.index = faiss.read_index(os.path.join(data_folder, "game_index.bin"))
    models.ft_model = compress_fasttext.models.CompressedFastTextKeyedVectors.load(os.path.join(data_folder, "cc.en.300.compressed.bin"))

    yield

    models.index = None
    models.ft_model = None



app = FastAPI(lifespan=lifespan)


origins = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1, http://localhost:5173, https://silverrecs.pages.dev, https://silverrecs.com, https://www.silverrecs.com")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(steam_api_router)
app.include_router(auth_router)
app.include_router(ml_router)








