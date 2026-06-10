# RAG Notebook Architecture Comparison

This document compares the current saved versions of:

- `notebooks/rag_cleaned.ipynb`
- `notebooks/RAG_helper.ipynb`

Both notebooks currently implement the same simple OpenAI call flow. They do not yet run the full RAG pipeline from `ingest.py` and `rag_helper.py`.

## `notebooks/rag_cleaned.ipynb`

```mermaid
flowchart TD
    A["Notebook start"] --> B["Import load_dotenv, OpenAI, os"]
    B --> C["Load .env"]
    C --> D{"OPENAI_API_KEY exists?"}
    D -- "No" --> E["Raise RuntimeError"]
    D -- "Yes" --> F["Create OpenAI client"]
    F --> G["Define llm(prompt)"]
    G --> H["Call llm with a test greeting"]
    H --> I["OpenAI Responses API"]
    I --> J["Return response.output_text"]
```

## `notebooks/RAG_helper.ipynb`

```mermaid
flowchart TD
    A["Notebook start"] --> B["Import load_dotenv, OpenAI, os"]
    B --> C["Load .env"]
    C --> D{"OPENAI_API_KEY exists?"}
    D -- "No" --> E["Raise RuntimeError"]
    D -- "Yes" --> F["Create OpenAI client"]
    F --> G["Define llm(prompt)"]
    G --> H["Call llm with a test greeting"]
    H --> I["OpenAI Responses API"]
    I --> J["Return response.output_text"]
```

## Comparison

| Area | `notebooks/rag_cleaned.ipynb` | `notebooks/RAG_helper.ipynb` | Difference |
| --- | --- | --- | --- |
| Environment loading | Uses `load_dotenv(".env")` | Uses `load_dotenv(".env")` | None |
| API client | Creates `OpenAI()` | Creates `OpenAI()` | None |
| API key validation | Checks `OPENAI_API_KEY` | Checks `OPENAI_API_KEY` | None |
| LLM helper | Defines `llm(prompt)` | Defines `llm(prompt)` | None |
| Model | `gpt-5.4-mini` | `gpt-5.4-mini` | None |
| RAG retrieval | Not present | Not present | None |
| Indexing | Not present | Not present | None |
| External course FAQ data | Not present | Not present | None |

## Current Architecture Summary

The current notebooks are LLM call notebooks, not full RAG notebooks. They validate the API key and send one prompt directly to the OpenAI Responses API.

```mermaid
flowchart LR
    U["User prompt"] --> N["Notebook llm() function"]
    N --> O["OpenAI Responses API"]
    O --> A["Answer text"]
```

## Intended Full RAG Architecture

The project already has helper code for a fuller RAG pipeline:

- `ingest.py` loads FAQ data and builds a `minsearch.Index`.
- `rag_helper.py` defines `RAGBase`, which searches the index, builds context, builds a prompt, and calls the OpenAI Responses API.

```mermaid
flowchart TD
    Q["User question"] --> R["RAGBase.rag(question)"]
    R --> S["Search minsearch index"]
    S --> C["Build context from top FAQ matches"]
    C --> P["Build prompt with question + context"]
    P --> L["OpenAI Responses API"]
    L --> A["Answer grounded in FAQ context"]

    D["DataTalks FAQ JSON"] --> I["load_faq_data()"]
    I --> B["build_index(documents)"]
    B --> S
```

## RAG Assistant Workflow

This is the higher-level workflow view of the RAG assistant. It separates the user-facing assistant from the knowledge base and shows how retrieved documents become context for the LLM.

```mermaid
flowchart TD
    subgraph KB["Knowledge Base"]
        DB[("FAQ database or search index")]
    end

    subgraph APP["RAG Assistant"]
        U["User"] -->|"Question"| A["Application"]
        A -->|"Query"| DB
        DB -->|"Retrieved data"| D["Top matching documents D1 to D5"]
        D --> A
        A --> P["Build prompt from question and context"]
        P --> L["LLM"]
        L --> ANS["Answer"]
        ANS --> U
    end
```

### Workflow Mapping

| Workflow step | Current project component |
| --- | --- |
| User asks a question | Notebook cell or application entry point |
| Application receives question | `RAGBase.rag(question)` |
| Query knowledge base | `RAGBase.search()` |
| Knowledge base | `minsearch.Index` built by `build_index(documents)` |
| Retrieved documents | Search results from FAQ records |
| Build prompt | `RAGBase.build_prompt()` with `PROMPT_TEMPLATE` |
| Call LLM | `RAGBase.llm()` using OpenAI Responses API |
| Return answer | `response.output_text` |

## Recommendation

Keep `notebooks/rag_cleaned.ipynb` as the minimal OpenAI smoke test notebook.

Use `notebooks/RAG_helper.ipynb` for the full RAG workflow by adding cells that import and use:

```python
from ingest import load_faq_data, build_index
from rag_helper import RAGBase
```

Then instantiate:

```python
documents = load_faq_data()
index = build_index(documents)
assistant = RAGBase(index=index, llm_client=openai_client)
assistant.rag("I just discovered the course. Can I join now?")
```
