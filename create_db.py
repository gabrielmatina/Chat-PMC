from app.config import PASTA_BASE_DOCUMENTOS
from app.rag.loader import carregar_todos_documentos
from app.rag.splitter import dividir_em_chunks
from app.rag.database import criar_banco_vetorial

def executar_ingestao():
    print("Iniciando pipeline de ingestão modular...")
    docs = carregar_todos_documentos(PASTA_BASE_DOCUMENTOS)
    if not docs:
        print("[Aviso] Nenhum documento encontrado na pasta base.")
        return
    
    chunks = dividir_em_chunks(docs)
    criar_banco_vetorial(chunks)
    print("Ingestão concluída com sucesso!")

if __name__ == "__main__":
    executar_ingestao()