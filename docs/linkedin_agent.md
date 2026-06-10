# Daily LinkedIn Agent

This project includes a small local agent for learning-in-public updates:

```text
scripts/daily_linkedin_agent.py
```

The agent generates a daily LinkedIn-ready Markdown draft from local repository progress. It does not post automatically by default. This is intentional: direct LinkedIn publishing requires separate LinkedIn API credentials and should not be hardcoded into the repository.

LinkedIn profile:

```text
https://www.linkedin.com/in/stephen-waigi-4a5ba1275/
```

## What It Does

The agent reads:

- Git commits from a selected time window.
- Files changed by those commits.
- Current uncommitted files that still need review.
- The latest entry in `docs/learning_log.md`.

It writes:

```text
docs/public_posts/YYYY-MM-DD-linkedin.md
```

The draft includes:

- progress summary
- repo artifacts
- reflection section
- LinkedIn post text
- course submission checklist

## Run It Manually

From the project root:

```bash
python scripts/daily_linkedin_agent.py
```

The default window is `yesterday 21:00`, which fits a daily 9:00 PM review cadence. Use a different git time window when needed:

```bash
python scripts/daily_linkedin_agent.py --since "midnight"
```

Use a specific post date:

```bash
python scripts/daily_linkedin_agent.py --date 2026-06-10
```

## Daily Workflow

1. Work on the project.
2. Commit meaningful progress.
3. Add or update `docs/learning_log.md`.
4. Run the agent at 9:00 PM.
5. Review the generated draft in `docs/public_posts/`.
6. Publish manually on LinkedIn from the profile above.
7. Submit the published link through the course platform.
8. Update the tracker in `docs/learning_in_public.md`.

## Approval Workflow

The generated Markdown file is the approval queue. Review and edit the `## LinkedIn Post` section before publishing it manually.

LinkedIn does not provide a simple personal-profile "private post for approval" workflow through this repo. Treat the local draft as the private approval copy. If LinkedIn API publishing is added later, keep the same draft-first approval step and only publish after explicit confirmation.

## Automation Option

For local daily reminders, schedule the script with cron:

```cron
0 21 * * * cd /mnt/d/Projects/llm-zoomcamp-2026-codesteve && .venv/bin/python scripts/daily_linkedin_agent.py
```

This creates a draft each day at 21:00 local machine time.

## Why It Does Not Auto-Post Yet

Auto-posting directly to LinkedIn requires:

- a LinkedIn developer app
- an access token with publishing permissions
- a safe credential storage strategy
- error handling for failed or duplicate posts
- a review policy so low-quality drafts are not published automatically

The current agent keeps the learning workflow reliable without risking accidental posts or leaked credentials.

## Future Extension

A future `--publish` mode can be added after credentials are configured safely through environment variables such as:

```text
LINKEDIN_ACCESS_TOKEN
LINKEDIN_AUTHOR_URN
```

Until then, use the generated Markdown as the reviewed source for manual LinkedIn posts.
