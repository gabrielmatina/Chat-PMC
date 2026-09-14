import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

CAMINHO_DB = "db"

PROMPT_LEGAL = """Você é um assistente jurídico especializado em análise de legislação e normas.
Sua função é responder à dúvida do usuário com estrita precisão e fidelidade ao contexto fornecido.

Diretrizes obrigatórias:
1. Baseie sua resposta estritamente nas informações fornecidas no contexto abaixo.
2. Sempre cite os artigos, parágrafos, incisos ou alíneas pertinentes quando estiverem disponíveis no texto.
3. Se a informação não constar no contexto, declare explicitamente: "A legislação fornecida não contém informações suficientes para responder a esta pergunta." Não deduza nem invente regras.

Contexto da Legislação:
{base_conhecimento}

Pergunta do Usuário:
{pergunta}

Resposta Objetiva e Fundamentada:"""

def inicializar_recursos():
    """Carrega o modelo de embeddings e o banco vetorial."""
    if not os.path.exists(CAMINHO_DB):
        raise FileNotFoundError(
            f"O diretório '{CAMINHO_DB}' não existe. Execute o script 'create_db.py' primeiro."
        )
    
    funcao_embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return db, llm

def consultar_lei(pergunta: str, db: Chroma, llm: ChatOpenAI):
    """Executa a busca por similaridade e gera a resposta via LLM."""
    # Busca com score de relevância (score varia de 0 a 1 em similaridade de cosseno)
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=4)

    if not resultados:
        print("\n[Aviso] Nenhum trecho foi retornado do banco vetorial.")
        return

    score_maximo = resultados[0][1]
    print(f"\n[Debug] Maior score de relevância encontrado: {score_maximo:.3f}")

    # Limiar ajustado para 0.60 para evitar falsos negativos em linguagem jurídica
    if score_maximo < 0.60:
        print("\n[Aviso] A pergunta não encontrou correspondência com relevância mínima na base.")
        return

    # Montagem do contexto com metadados (se disponíveis)
    blocos_texto = []
    for doc, score in resultados:
        origem = doc.metadata.get("source", "Documento")
        pagina = doc.metadata.get("page", "?")
        blocos_texto.append(f"[Fonte: {origem} | Pág: {pagina} | Relevância: {score:.2f}]\n{doc.page_content}")

    base_conhecimento = "\n\n---\n\n".join(blocos_texto)

    prompt = ChatPromptTemplate.from_template(PROMPT_LEGAL)
    cadeia = prompt | llm
    
    resposta = cadeia.invoke({
        "pergunta": pergunta,
        "base_conhecimento": base_conhecimento
    })

    print("\n" + "=" * 50)
    print("RESPOSTA DA IA:")
    print("=" * 50)
    print(resposta.content)
    print("=" * 50)

def main():
    try:
        db, llm = inicializar_recursos()
    except Exception as e:
        print(f"Erro ao inicializar base de dados: {e}")
        return

    print("=== Consultor de Legislação RAG Ativo ===")
    print("Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("\nEscreva sua pergunta sobre a lei: ").strip()
        if not pergunta:
            continue
        if pergunta.lower() in ("sair", "exit", "quit"):
            print("Encerrando...")
            break
        
        consultar_lei(pergunta, db, llm)

if __name__ == "__main__":
    main()