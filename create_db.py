import shutil
import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

PASTA_BASE = "base"
CAMINHO_DB = "db"

def carregar_documentos():
    carregador = PyPDFDirectoryLoader(PASTA_BASE)
    return carregador.load()

def dividir_chunks(documentos):
    # Separadores priorizando a estrutura de leis e parágrafos
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size=800,       # Reduzido de 2000 para evitar diluição semântica
        chunk_overlap=150,    # Margem suficiente para manter conexões
        length_function=len,
        add_start_index=True,
        separators=["\n\nArt. ", "\nArt. ", "\n\n", "\n", " ", ""]
    )
    chunks = separador_documentos.split_documents(documentos)
    print(f"Total de chunks gerados: {len(chunks)}")
    return chunks

def vetorizar_chunks(chunks):
    # Apaga o banco anterior se existir para aplicar a nova métrica de distância do zero
    if os.path.exists(CAMINHO_DB):
        shutil.rmtree(CAMINHO_DB)
        print("Banco anterior removido para recriação.")

    funcao_embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Configuração crítica: 'hnsw:space': 'cosine' para normalizar o score de 0 a 1
    db = Chroma.from_documents(
        documents=chunks,
        embedding=funcao_embedding,
        persist_directory=CAMINHO_DB,
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("Banco de Dados criado com sucesso usando Similaridade de Cosseno!")

def criar_db():
    documentos = carregar_documentos()
    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)

if __name__ == "__main__":
    criar_db()