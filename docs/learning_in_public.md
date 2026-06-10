# Learning in Public Workflow

This repository is the source of truth for my LLM Zoomcamp learning-in-public work.

DataTalksClub recommends sharing progress after completing a unit, module, homework, or project. The post should include the course hashtag, tag DataTalks.Club and the lead instructor, and then be submitted through the course platform. Accepted links count toward leaderboard points.

References:

- DataTalksClub Learning in Public: https://datatalks.club/docs/courses/zoomcamp-logistics/learning-in-public/
- DataTalksClub Leaderboard: https://datatalks.club/docs/courses/zoomcamp-logistics/leaderboard/

## Goals

- Reinforce learning by explaining concepts publicly.
- Build a visible portfolio of LLM/RAG work.
- Track experiments, errors, fixes, and design decisions.
- Create social posts that can be submitted for course leaderboard credit.

## Weekly Cadence

| Day | Activity | Output |
| --- | --- | --- |
| Learning day | Work through lessons, notebooks, or experiments. | Code, notebook updates, short notes. |
| Reflection day | Summarize what changed and what was learned. | `docs/learning_log.md` entry. |
| Publishing day | Turn the learning entry into a public post. | LinkedIn/X post using `docs/post_templates.md`. |
| Submission day | Submit the public post link through the course platform. | Update the submission tracker below. |

## Publishing Checklist

Before publishing a post:

- The post explains one concrete thing learned.
- The post includes the course hashtag: `#llmzoomcamp`.
- The post links to a relevant repo file, notebook, diagram, or commit.
- The post mentions the challenge, fix, or insight, not only that work was completed.
- The post avoids secrets, API keys, private tokens, and local `.env` values.
- The post is submitted through the course platform after publishing.

## Submission Tracker

| Date | Topic | Public link | Platform submitted? | Accepted? | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-06-10 | RAG notebook setup and OpenAI smoke test | TBD | No | No | Initial notebooks and environment fixes. |
| 2026-06-10 | Elasticsearch retrieval layer for RAG | TBD | No | No | Added Docker Elasticsearch workflow and comparison notebook. |
| 2026-06-10 | FAQ database schema documentation | TBD | No | No | Documented SQLite schema and FTS5 structure. |

## Content Backlog

| Topic | Angle | Repo artifact |
| --- | --- | --- |
| OpenAI smoke-test notebook | How I debugged API key, provider mismatch, and model access issues. | `notebooks/rag_cleaned.ipynb` |
| RAG helper class | Moving notebook logic into reusable project code. | `rag_helper.py` |
| FAQ schema | Understanding how course FAQ data is stored and searched. | `docs/faq_db_schema.md` |
| RAG architecture | Comparing simple LLM calls with a full retrieval-augmented workflow. | `docs/rag_architecture_comparison.md` |
| Elasticsearch layer | Adding a production-style retrieval backend for learning. | `notebooks/elasticsearch_rag.ipynb` |

## Post Format

Use this structure for most posts:

1. What I worked on.
2. What broke or confused me.
3. What I changed.
4. What I learned.
5. Link to repo artifact.
6. Hashtag and tags.

## Maintenance Rules

- Add a learning-log entry before writing a social post.
- Keep posts tied to specific repo artifacts.
- Update the submission tracker after publishing and after course moderation.
- Prefer small, frequent posts over large summary posts.
- Do not commit generated local artifacts such as `faq.db`.
