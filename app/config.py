import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_BASE_DOCUMENTOS = BASE_DIR / "base"
CAMINHO_CHROMA = str(BASE_DIR / "db")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODELO_EMBEDDING = "text-embedding-3-small"
MODELO_LLM = "gpt-4o-mini"