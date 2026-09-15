import os
import shutil
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import CAMINHO_CHROMA, MODELO_EMBEDDING

def obter_funcao_embedding():
    return OpenAIEmbeddings(model=MODELO_EMBEDDING)

def criar_banco_vetorial(chunks: List[Document]) -> Chroma:
    if os.path.exists(CAMINHO_CHROMA):
        shutil.rmtree(CAMINHO_CHROMA)
        print("Banco anterior excluído para atualização completa.")

    db = Chroma.from_documents(
        documents=chunks,
        embedding=obter_funcao_embedding(),
        persist_directory=CAMINHO_CHROMA,
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("Novo banco vetorial Chroma criado com sucesso!")
    return db

def carregar_banco_existente() -> Chroma:
    if not os.path.exists(CAMINHO_CHROMA):
        raise FileNotFoundError("Base vetorial não encontrada. Execute a ingestão primeiro.")
        
    return Chroma(
        persist_directory=CAMINHO_CHROMA,
        embedding_function=obter_funcao_embedding(),
        collection_metadata={"hnsw:space": "cosine"}
    )