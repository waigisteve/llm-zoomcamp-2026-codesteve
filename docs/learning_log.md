# Learning Log

Chronological notes for LLM Zoomcamp learning-in-public posts.

## 2026-06-15 - RAG Helper Expanded into Agentic RAG Experiments

### What I worked on

- Expanded `notebooks/RAG_helper.ipynb` from a minimal OpenAI helper into a larger notebook with `RAGBase`, retrieval calls, tool-calling patterns, and agent-loop experiments.
- Kept `notebooks/elasticsearch_rag.ipynb` aligned with the broader retrieval experiments.
- Added dependency updates in `pyproject.toml` and `uv.lock` to support the newer agent and AI experiments.

### What changed

- The helper notebook moved beyond a single smoke test and now captures more of the course learning flow in one place.
- The repo now has a clearer progression from simple LLM calls to retrieval-backed answers and agent-style loops.
- The pushed commit for this work is `7dcd660`.

### What I learned

- A tiny helper notebook is useful at the start, but it becomes more valuable when it also documents the evolution toward full RAG and agent workflows.
- Keeping retrieval and orchestration concepts visible in notebook steps makes experiments easier to revisit and explain.
- Dependency changes should be committed alongside notebook workflow changes so the environment matches the learning artifact.

### Repo artifacts

- `notebooks/RAG_helper.ipynb`
- `notebooks/elasticsearch_rag.ipynb`
- `pyproject.toml`

### Draft post status

- Public post: Drafted
- Course platform submitted: No

## 2026-06-10 - OpenAI Smoke Test and Notebook Cleanup

### What I worked on

- Created minimal notebooks for testing `.env` loading and the OpenAI Responses API.
- Moved notebooks into the `notebooks/` directory.
- Added markdown headings to make each notebook easier to follow.

### What broke

- The notebook initially mixed an OpenAI API key with a Groq-compatible `base_url`, which caused authentication errors.
- Some notebook cells had stale state after kernel restarts.

### What I learned

- Keep provider configuration explicit.
- Restarting the kernel and running cells top-to-bottom is important when debugging notebooks.
- A small smoke-test notebook is useful before building a larger RAG flow.

### Repo artifacts

- `notebooks/rag_cleaned.ipynb`
- `notebooks/RAG_helper.ipynb`

### Draft post status

- Public post: TBD
- Course platform submitted: No

## 2026-06-10 - RAG Architecture and FAQ Schema

### What I worked on

- Added architecture diagrams for the RAG assistant workflow.
- Documented the local `faq.db` SQLite schema.
- Identified the FTS5 search tables and the primary `docs` table.

### What broke

- Mermaid diagrams failed on GitHub when node labels contained escaped quotes.

### What I learned

- Mermaid labels should stay simple for GitHub rendering.
- SQLite FTS5 creates several internal backing tables that should be documented but not manually edited.

### Repo artifacts

- `docs/rag_architecture_comparison.md`
- `docs/faq_db_schema.md`

### Draft post status

- Public post: TBD
- Course platform submitted: No

## 2026-06-10 - Elasticsearch Retrieval Layer

### What I worked on

- Added an Elasticsearch retrieval wrapper with a `search()` interface compatible with `RAGBase`.
- Created an Elasticsearch RAG notebook.
- Documented Docker setup, notebook run order, retrieval comparison, and troubleshooting.

### What broke

- `localhost:9200` did not resolve until Elasticsearch was running in Docker.
- Docker needed WSL integration before it was usable from the WSL terminal.

### What I learned

- Elasticsearch can be introduced as a retriever without rewriting the RAG pipeline.
- Keeping a common `search()` interface makes it easy to compare `minsearch` and Elasticsearch.
- Docker service readiness should be verified before running notebook cells.

### Repo artifacts

- `elastic_search.py`
- `notebooks/elasticsearch_rag.ipynb`
- `docs/elasticsearch_layer.md`

### Draft post status

- Public post: TBD
- Course platform submitted: No
