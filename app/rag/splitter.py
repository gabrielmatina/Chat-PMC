from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def dividir_em_chunks(documentos: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
        add_start_index=True,
        separators=["\n\nArt. ", "\nArt. ", "\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_documents(documentos)
    
    # Truque de enriquecimento: injeta a origem dentro do texto pesquisável
    for chunk in chunks:
        doc_ref = chunk.metadata.get("documento", "Legislação")
        chunk.page_content = f"[{doc_ref}]\n{chunk.page_content}"
        
    print(f"Total de chunks gerados: {len(chunks)}")
    return chunks