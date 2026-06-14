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

🚀 Module `[number]` of LLM Zoomcamp by `@DataTalksClub` complete!

Just finished `[module/topic]`. Learned how to:

- ✅ `[skill 1]`
- ✅ `[skill 2]`
- ✅ `[skill 3]`
- ✅ `[skill 4]`

Here's my homework solution: `[link]`

Following along with this amazing free course by `@Alexey Grigorev` — who else is learning to build with LLMs?

You can sign up here: `https://github.com/DataTalksClub/llm-zoomcamp/`

`#llmzoomcamp` `#LearningInPublic`

## Template 4: Twitter/X Module Post

🤖 Module `[number]` of `#llmzoomcamp` done!

Learned how to:
- `[skill 1]`
- `[skill 2]`
- `[skill 3]`

Homework: `[link]`

Thanks `@DataTalksClub` and `@Al_Grigor`

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

## Draft: Module 1 Completion

🚀 Module 1 of LLM Zoomcamp by `@DataTalksClub` complete!

Just finished Module 1 - Agentic RAG. Learned how to:

- ✅ Build a RAG system from scratch in plain Python
- ✅ Index and search documents with `minsearch`
- ✅ Compare retrieval approaches with Elasticsearch
- ✅ Turn the RAG pipeline into an agent with function calling

Here's my homework solution: `https://github.com/waigisteve/llm-zoomcamp-2026-codesteve/blob/main/notebooks/RAG_helper.ipynb`

Following along with this amazing free course by `@Alexey Grigorev` — who else is learning to build with LLMs?

You can sign up here: `https://github.com/DataTalksClub/llm-zoomcamp/`

`#llmzoomcamp` `#RAG` `#LearningInPublic`
