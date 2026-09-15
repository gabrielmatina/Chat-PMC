import os
import re
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader

PADRAO_NOME_ARQUIVO = re.compile(r"^(?P<tipo>[A-Z]+)_(?P<numero>\d+)_(?P<ano>\d+)", re.IGNORECASE)

MAPA_TIPOS = {
    "DEC": "Decreto Municipal",
    "LC": "Lei Complementar",
    "LEI": "Lei Ordinária"
}

def extrair_metadados_nome(caminho_arquivo: Path) -> dict:
    """Extrai tipo, número e ano a partir do nome padrão (ex: DEC_880_2008)."""
    nome_sem_extensao = caminho_arquivo.stem
    match = PADRAO_NOME_ARQUIVO.match(nome_sem_extensao)
    
    if match:
        dados = match.groupdict()
        tipo_sigla = dados["tipo"].upper()
        return {
            "documento": f"{tipo_sigla} {dados['numero']}/{dados['ano']}",
            "tipo_extenso": MAPA_TIPOS.get(tipo_sigla, "Legislação"),
            "tipo_sigla": tipo_sigla,
            "numero": dados["numero"],
            "ano": dados["ano"],
            "arquivo": caminho_arquivo.name
        }
    
    return {
        "documento": nome_sem_extensao,
        "tipo_extenso": "Legislação",
        "tipo_sigla": "OUTRO",
        "numero": "S/N",
        "ano": "S/D",
        "arquivo": caminho_arquivo.name
    }

def carregar_todos_documentos(diretorio_base: Path) -> List[Document]:
    """Varre todas as subpastas e carrega arquivos MD, TXT e PDF."""
    documentos_totais = []
    
    for caminho in diretorio_base.rglob("*"):
        if not caminho.is_file():
            continue
            
        extensao = caminho.suffix.lower()
        docs_carregados = []
        
        try:
            if extensao in [".md", ".txt"]:
                loader = TextLoader(str(caminho), encoding="utf-8")
                docs_carregados = loader.load()
            elif extensao == ".pdf":
                loader = PyPDFLoader(str(caminho))
                docs_carregados = loader.load()
            else:
                continue
        except Exception as e:
            print(f"[Erro] Falha ao carregar {caminho.name}: {e}")
            continue

        metadados_base = extrair_metadados_nome(caminho)
        
        for doc in docs_carregados:
            # Mescla metadados do arquivo aos metadados do documento
            doc.metadata.update(metadados_base)
            documentos_totais.append(doc)
            
    print(f"Total de documentos/páginas carregados: {len(documentos_totais)}")
    return documentos_totais