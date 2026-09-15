# 🏛️ Chat-PMC: Consultor Inteligente de Legislação Municipal

Sistema de consulta em linguagem natural e fundamentação jurídica sobre a legislação do Município de Contagem, baseado em arquitetura **RAG (Retrieval-Augmented Generation)** com modelos de linguagem e bancos vetoriais.

---

## 📌 Histórico de Versões & Status Atual

### 🟢 v0.1 — Prova de Conceito (MVP Atual)
Primeira iteração funcional focada na validação da pipeline básica de ingestão e recuperação vetorial sobre o **Decreto Municipal nº 880/2008** (Avaliação Especial de Desempenho no Estágio Probatório).

- **Status da Pipeline:** Ingestão de PDF (`PyPDFDirectoryLoader`), divisão de texto com `RecursiveCharacterTextSplitter` e indexação no **ChromaDB**.
- **Modelos:** Embeddings com `text-embedding-3-small` e geração de resposta com `gpt-4o-mini` (OpenAI).
- **Interface Atual:** Terminal interativo via VS Code.
- **Diagnóstico Técnico & Limitações Encontradas:**
  - Recuperação semântica com oscilação de score de similaridade (35% a 72%).
  - Divisão de texto em tamanho fixo (`chunk_size=800`, `chunk_overlap=150`) causa diluição de sentido e fragmenta artigos, parágrafos e incisos interdependentes.
  - Inexistência de metadados granulares (o sistema referencia páginas, mas não identifica artigos ou normas específicas).
  - Incapacidade de responder a consultas quantitativas globais (ex.: total de artigos ou normas vigentes).

---

## 🗺️ Roadmap de Evolução e Próximos Passos

[v0.1 MVP] ➔ [Etapa 1: Ingestão Modular] ➔ [Etapa 2: RAG Jurídico] ➔ [Etapa 3: Roteamento & Híbrido] ➔ [Etapa 4: API & Web] ➔ [Etapa 5: Produção & Métricas]

### 🔲 Etapa 1: Fundação & Pipeline de Ingestão Modular
Transformar os scripts monolíticos (`create_db.py` e `main.py`) em uma estrutura modular pronta para dezenas de documentos:
- [X] Modularização do código em pastas estruturadas (`app/rag/`, `app/prompts/`, `base/`).
- [X] Organização do diretório de documentos por categorias normativas: `base/leis/`, `base/leis_complementares/`, `base/decretos/`.
- [X] Extração e injeção automática de metadados de arquivo (tipo de ato, número, ano e município).

### 🔲 Etapa 2: Chunking Semântico Jurídico e Camada Estrutural
Substituição da divisão cega de caracteres por preservação de unidades normativas do direito administrativo:
- [ ] Implementação de **Legal Text Splitter** preservando blocos indivisíveis: Artigo + Parágrafos + Incisos + Alíneas.
- [ ] Enriquecimento de metadados por chunk: `{"norma": "Dec. 880/2008", "artigo": "13", "tema": "etapas_avaliacao"}`.
- [ ] Criação de índice estrutural de catálogo para mapeamento de ementas, vigências e contagens semânticas.

### 🔲 Etapa 3: Roteamento de Consultas & Recuperação Avançada (Advanced RAG)
Aumento da acurácia e eliminação de alucinações causadas pelo crescimento da base documental:
- [ ] **Router de Intenção:** Classificação da dúvida em Específica (Vetorial), Estrutural (Metadados) ou Temática Ampla.
- [ ] **Busca Híbrida:** Fusão de busca vetorial (similaridade de cosseno) com busca léxica (**BM25**) para precisão de artigos e prazos exatos.
- [ ] **Re-ranking (Cross-Encoder):** Reordenação dos candidatos recuperados para enviar ao LLM apenas trechos com alta relevância.
- [ ] **Pipeline de Avaliação:** Criação de conjunto de testes (`tests/benchmark.json`) para mensurar métricas de *Answer Relevance*, *Faithfulness* e *Recall*.

### 🔲 Etapa 4: Desacoplamento de Backend (FastAPI) e Frontend Moderno
Transição do terminal para uma aplicação web com separação de responsabilidades:
- [ ] **Backend (FastAPI):** Endpoints REST para `/ask`, `/documents`, `/filters` e streaming de tokens.
- [ ] **Frontend (React + Vite + Tailwind CSS):** Interface inspirada no Gemini/ChatGPT, com exibição colapsável de citações, artigos e filtros laterais por tipo de norma e ano.

### 🔲 Etapa 5: Preparação para Produção e Orquestração de Agentes
Empacotamento profissional da solução para portfólio:
- [ ] Conteinerização completa da aplicação com **Docker** e **Docker Compose**.
- [ ] Preparação da arquitetura para transição para **LangGraph** (agentes autônomos com memória conversacional persistente e ferramentas especializadas).

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| **Linguagem & Runtime** | Python 3.11+ |
| **Framework RAG / Orquestração** | LangChain / LangChain Community / LangGraph |
| **Modelos de IA** | OpenAI (`gpt-4o-mini`, `text-embedding-3-small`) |
| **Vector Store** | ChromaDB (métrica de distância: Cosseno) |
| **Controle de Versão** | Git & GitHub |
