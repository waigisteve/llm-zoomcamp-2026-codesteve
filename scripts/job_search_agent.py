from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

import requests


DEFAULT_KEYWORDS = [
    "data analyst",
    "analytics engineer",
    "database administrator",
    "data tech lead",
    "devops engineer",
    "ai engineer",
    "genai engineer",
    "generative ai engineer",
]

DEFAULT_SOURCES = ["remotive", "arbeitnow", "remoteok"]
REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class JobPost:
    title: str
    company: str
    location: str
    url: str
    source: str
    keyword: str
    published_at: str | None = None
    salary: str | None = None
    tags: tuple[str, ...] = ()


def fetch_remotive(keyword: str, limit: int) -> list[JobPost]:
    url = f"https://remotive.com/api/remote-jobs?search={quote_plus(keyword)}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    jobs = []
    for item in response.json().get("jobs", []):
        text = searchable_text(
            item.get("title", ""),
            item.get("company_name", ""),
            item.get("candidate_required_location", ""),
            item.get("description", ""),
            " ".join(item.get("tags") or []),
        )
        if not is_relevant(keyword, text):
            continue

        jobs.append(
            JobPost(
                title=item.get("title", "").strip(),
                company=item.get("company_name", "").strip(),
                location=item.get("candidate_required_location", "Remote").strip(),
                url=item.get("url", "").strip(),
                source="remotive",
                keyword=keyword,
                published_at=item.get("publication_date"),
                salary=item.get("salary") or None,
                tags=tuple(item.get("tags") or ()),
            )
        )

        if len(jobs) >= limit:
            break

    return jobs


def fetch_arbeitnow(keyword: str, limit: int) -> list[JobPost]:
    response = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=30)
    response.raise_for_status()
    keyword_lower = keyword.lower()

    jobs = []
    for item in response.json().get("data", []):
        text = searchable_text(
            item.get("title", ""),
            item.get("company_name", ""),
            item.get("location", ""),
            " ".join(item.get("tags") or []),
        )

        if not is_relevant(keyword_lower, text):
            continue

        created_at = item.get("created_at")
        published_at = None
        if isinstance(created_at, int):
            published_at = datetime.fromtimestamp(created_at, tz=timezone.utc).date().isoformat()

        jobs.append(
            JobPost(
                title=item.get("title", "").strip(),
                company=item.get("company_name", "").strip(),
                location=item.get("location", "Not specified").strip(),
                url=item.get("url", "").strip(),
                source="arbeitnow",
                keyword=keyword,
                published_at=published_at,
                tags=tuple(item.get("tags") or ()),
            )
        )

        if len(jobs) >= limit:
            break

    return jobs


def fetch_remoteok(keyword: str, limit: int) -> list[JobPost]:
    headers = {"User-Agent": "llm-zoomcamp-job-search-agent/0.1"}
    response = requests.get("https://remoteok.com/api", headers=headers, timeout=30)
    response.raise_for_status()
    keyword_lower = keyword.lower()

    jobs = []
    for item in response.json()[1:]:
        text = searchable_text(
            item.get("position", ""),
            item.get("company", ""),
            item.get("location", ""),
            item.get("description", ""),
            " ".join(item.get("tags") or []),
        )

        if not is_relevant(keyword_lower, text):
            continue

        salary_parts = [str(item.get("salary_min") or ""), str(item.get("salary_max") or "")]
        salary = " - ".join(part for part in salary_parts if part)

        jobs.append(
            JobPost(
                title=item.get("position", "").strip(),
                company=item.get("company", "").strip(),
                location=item.get("location", "Remote").strip(),
                url=item.get("url", "").strip(),
                source="remoteok",
                keyword=keyword,
                published_at=item.get("date"),
                salary=salary or None,
                tags=tuple(item.get("tags") or ()),
            )
        )

        if len(jobs) >= limit:
            break

    return jobs


def fetch_jobs(keywords: list[str], sources: list[str], limit_per_keyword: int) -> list[JobPost]:
    source_fetchers = {
        "remotive": fetch_remotive,
        "arbeitnow": fetch_arbeitnow,
        "remoteok": fetch_remoteok,
    }

    jobs = []
    for keyword in keywords:
        for source in sources:
            fetcher = source_fetchers[source]
            try:
                jobs.extend(fetcher(keyword, limit_per_keyword))
            except requests.RequestException as exc:
                print(f"warning: {source} failed for {keyword!r}: {exc}")

    return dedupe_jobs(jobs)


def dedupe_jobs(jobs: list[JobPost]) -> list[JobPost]:
    seen_urls = set()
    unique_jobs = []

    for job in jobs:
        if not job.url or job.url in seen_urls:
            continue
        seen_urls.add(job.url)
        unique_jobs.append(job)

    return unique_jobs


def searchable_text(*parts: str) -> str:
    return " ".join(part or "" for part in parts).lower()


def is_relevant(keyword: str, text: str) -> bool:
    keyword = keyword.lower().strip()
    text = text.lower()

    if keyword in text:
        return True

    terms = [term for term in re.findall(r"[a-z0-9]+", keyword) if len(term) > 2 or term == "ai"]
    if not terms:
        return False

    text_terms = set(re.findall(r"[a-z0-9]+", text))
    return any(term in text_terms for term in terms)


def write_json_report(jobs: list[JobPost], output_dir: Path, report_date: date) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report_date.isoformat()}-jobs.json"
    payload = [asdict(job) for job in jobs]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_markdown_report(
    jobs: list[JobPost],
    output_dir: Path,
    report_date: date,
    keywords: list[str],
    sources: list[str],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report_date.isoformat()}-jobs.md"

    lines = [
        f"# Job Search Report - {report_date.isoformat()}",
        "",
        "## Search Scope",
        "",
        f"- Keywords: {', '.join(keywords)}",
        f"- Sources: {', '.join(sources)}",
        f"- Total unique jobs: {len(jobs)}",
        "",
        "## Results",
        "",
    ]

    if not jobs:
        lines.append("No matching jobs found. Try broader keywords or fewer filters.")
    else:
        for index, job in enumerate(jobs, start=1):
            lines.extend(
                [
                    f"### {index}. {job.title}",
                    "",
                    f"- Company: {job.company or 'Not specified'}",
                    f"- Location: {job.location or 'Not specified'}",
                    f"- Source: {job.source}",
                    f"- Matched keyword: {job.keyword}",
                    f"- Published: {job.published_at or 'Not specified'}",
                    f"- Salary: {job.salary or 'Not specified'}",
                    f"- Tags: {', '.join(job.tags) if job.tags else 'Not specified'}",
                    f"- Link: {job.url}",
                    "",
                ]
            )

    lines.extend(
        [
            "## Manual Search Links",
            "",
            "Use these for sites that should be searched manually rather than scraped directly:",
            "",
        ]
    )

    for keyword in keywords:
        encoded = quote_plus(keyword)
        lines.extend(
            [
                f"- LinkedIn {keyword}: https://www.linkedin.com/jobs/search/?keywords={encoded}",
                f"- Indeed {keyword}: https://www.indeed.com/jobs?q={encoded}",
                f"- Google Jobs {keyword}: https://www.google.com/search?q={encoded}+jobs",
            ]
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find job openings from public job APIs.")
    parser.add_argument(
        "--keyword",
        action="append",
        dest="keywords",
        help="Keyword to search. Can be repeated. Defaults to the built-in data/AI/devops list.",
    )
    parser.add_argument(
        "--source",
        action="append",
        choices=DEFAULT_SOURCES,
        dest="sources",
        help="Source to query. Can be repeated.",
    )
    parser.add_argument(
        "--limit-per-keyword",
        type=int,
        default=10,
        help="Maximum jobs per keyword per source.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Report date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "docs" / "job_reports",
        help="Directory for Markdown and JSON reports.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    keywords = args.keywords or DEFAULT_KEYWORDS
    sources = args.sources or DEFAULT_SOURCES
    report_date = datetime.strptime(args.date, "%Y-%m-%d").date()

    jobs = fetch_jobs(
        keywords=keywords,
        sources=sources,
        limit_per_keyword=args.limit_per_keyword,
    )
    markdown_path = write_markdown_report(jobs, args.output_dir, report_date, keywords, sources)
    json_path = write_json_report(jobs, args.output_dir, report_date)

    print(markdown_path)
    print(json_path)


if __name__ == "__main__":
    main()
