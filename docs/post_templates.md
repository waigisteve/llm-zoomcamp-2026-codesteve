# Learning in Public Post Templates

Use these drafts as starting points for LinkedIn or X posts. Replace placeholders before publishing.

## Template 1: Debugging Story

Today in `#llmzoomcamp`, I debugged `[problem]` while working on `[artifact]`.

What happened:
- `[symptom or error]`
- `[incorrect assumption]`
- `[root cause]`

What fixed it:
- `[fix 1]`
- `[fix 2]`

What I learned:
`[one clear lesson]`

Repo artifact: `[link]`

`#llmzoomcamp` `#RAG` `#LearningInPublic`

## Template 2: Architecture/Design Post

I added `[feature/layer]` to my LLM Zoomcamp project.

The architecture is:
`[short flow, for example: question -> retriever -> context -> prompt -> LLM -> answer]`

Why this matters:
- `[reason 1]`
- `[reason 2]`
- `[reason 3]`

The most useful design decision was `[decision]` because `[reason]`.

Repo artifact: `[link]`

`#llmzoomcamp` `#RAG` `#Elasticsearch` `#LearningInPublic`

## Template 3: Module Progress Post

Progress update for `#llmzoomcamp`:

This week I worked on `[topic]`.

Key takeaways:
- `[takeaway 1]`
- `[takeaway 2]`
- `[takeaway 3]`

The hardest part was `[challenge]`.
The next thing I want to improve is `[next step]`.

Repo artifact: `[link]`

`#llmzoomcamp` `#LearningInPublic`

## Draft: Elasticsearch RAG Layer

Today in `#llmzoomcamp`, I added Elasticsearch as a retrieval layer to my RAG learning project.

The flow is now:
question -> Elasticsearch search -> top FAQ documents -> prompt context -> OpenAI Responses API -> grounded answer.

What I learned:
- Elasticsearch needs to be running as a local service before the notebook can query `localhost:9200`.
- A common `search()` interface makes it easier to compare `minsearch` and Elasticsearch.
- Field boosting lets me give more weight to FAQ questions than sections or answers.

Repo artifacts:
- `elastic_search.py`
- `notebooks/elasticsearch_rag.ipynb`
- `docs/elasticsearch_layer.md`

`#llmzoomcamp` `#RAG` `#Elasticsearch` `#LearningInPublic`

## Draft: Notebook Debugging

Today in `#llmzoomcamp`, I cleaned up my RAG notebooks and fixed a few environment issues.

The main lesson: when debugging notebooks, separate the smallest possible smoke test from the full experiment.

What I fixed:
- API key loading from `.env`
- provider mismatch between OpenAI and Groq-compatible endpoints
- notebook organization under `notebooks/`
- markdown sections for easier review

Repo artifacts:
- `notebooks/rag_cleaned.ipynb`
- `notebooks/RAG_helper.ipynb`

`#llmzoomcamp` `#OpenAI` `#Jupyter` `#LearningInPublic`
