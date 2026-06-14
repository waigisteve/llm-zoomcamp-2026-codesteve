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

## Public Profile

LinkedIn: https://www.linkedin.com/in/stephen-waigi-4a5ba1275/

## Weekly Cadence

| Day | Activity | Output |
| --- | --- | --- |
| Learning day | Work through lessons, notebooks, or experiments. | Code, notebook updates, short notes. |
| Reflection day | Summarize what changed and what was learned. | `docs/learning_log.md` entry. |
| Publishing day | Turn the learning entry into a public post. | LinkedIn/X post using `docs/post_templates.md`. |
| Submission day | Submit the public post link through the course platform. | Update the submission tracker below. |

## Publishing Checklist

Before publishing a post:

- Prefer a clear milestone framing such as module complete, homework complete, or project complete.
- The post explains one concrete thing learned.
- The post lists 3-5 specific skills or concepts learned.
- The post includes the course hashtag: `#llmzoomcamp`.
- On LinkedIn, tag `@Alexey Grigorev` and `@DataTalksClub`.
- The post links to a relevant repo file, notebook, diagram, or commit.
- When possible, include a "homework solution" or repo artifact link directly in the body of the post.
- The post mentions the challenge, fix, or insight, not only that work was completed.
- End with a simple call to action or reflection, not just a status statement.
- The post avoids secrets, API keys, private tokens, and local `.env` values.
- The post is submitted through the course platform after publishing.

## Submission Tracker

| Date | Topic | Public link | Platform submitted? | Accepted? | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-06-15 | RAG helper expanded into agentic RAG experiments | TBD | No | No | Commit `7dcd660` expands the helper notebook into fuller RAG and agent-loop experiments. |
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

1. Milestone headline such as module complete or homework complete.
2. One-line summary of the topic.
3. Three to five concrete things learned.
4. Homework solution or repo artifact link.
5. Short closing reflection or question.
6. Hashtag and tags.

## Maintenance Rules

- Add a learning-log entry before writing a social post.
- Keep posts tied to specific repo artifacts.
- Update the submission tracker after publishing and after course moderation.
- Prefer small, frequent posts over large summary posts.
- Do not commit generated local artifacts such as `faq.db`.
