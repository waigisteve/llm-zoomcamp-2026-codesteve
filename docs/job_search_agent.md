# Job Search Agent

This project includes a local job-search agent:

```text
scripts/job_search_agent.py
```

It searches public job APIs, deduplicates results, and writes daily reports under:

```text
docs/job_reports/
```

## Roles Covered

Default keywords:

- data analyst
- analytics engineer
- database administrator
- data tech lead
- devops engineer
- ai engineer
- genai engineer
- generative ai engineer

## Sources

The current implementation uses public API-style sources:

- Remotive
- Arbeitnow
- RemoteOK

It also adds manual search links for sites that should not be scraped directly from this repo, such as LinkedIn and Indeed.

## Why Not Scrape LinkedIn Directly?

Many major job boards restrict automated scraping in their terms of service and actively block bots. For those sites, the agent generates direct search links instead of scraping pages.

Use the report as a daily review dashboard:

1. Review public API results.
2. Open the manual LinkedIn/Indeed/Google Jobs links.
3. Save or apply to relevant roles.
4. Track promising leads separately.

## Run the Agent

From the project root:

```bash
.venv/bin/python scripts/job_search_agent.py
```

Search one keyword:

```bash
.venv/bin/python scripts/job_search_agent.py --keyword "ai engineer"
```

Search multiple keywords:

```bash
.venv/bin/python scripts/job_search_agent.py \
  --keyword "database administrator" \
  --keyword "devops engineer" \
  --keyword "genai engineer"
```

Limit results:

```bash
.venv/bin/python scripts/job_search_agent.py --limit-per-keyword 5
```

Use selected sources:

```bash
.venv/bin/python scripts/job_search_agent.py --source remotive --source remoteok
```

## Outputs

The agent writes:

```text
docs/job_reports/YYYY-MM-DD-jobs.md
docs/job_reports/YYYY-MM-DD-jobs.json
```

The Markdown report is for human review. The JSON report is for later automation, filtering, or dashboards.

## Daily Schedule

To run it every morning at 8:00 AM:

```cron
0 8 * * * cd /mnt/d/Projects/llm-zoomcamp-2026-codesteve && .venv/bin/python scripts/job_search_agent.py >> docs/job_reports/job_agent.log 2>&1
```

## Suggested Review Workflow

1. Open the latest Markdown report in `docs/job_reports/`.
2. Scan for relevant roles.
3. Open the job links.
4. Open the manual LinkedIn/Indeed links for the same keywords.
5. Track applications in a spreadsheet, Notion page, or a future `docs/job_applications.md`.

## Future Improvements

- Add location filters.
- Add remote-only filters.
- Add salary filters.
- Add email or Windows notifications.
- Add scoring based on preferred tech stack.
- Add an applications tracker.
