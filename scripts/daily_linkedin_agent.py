from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


DEFAULT_HASHTAGS = ["#llmzoomcamp", "#RAG", "#LearningInPublic"]
LINKEDIN_PROFILE_URL = "https://www.linkedin.com/in/stephen-waigi-4a5ba1275/"
DEFAULT_SINCE = "yesterday 21:00"


@dataclass(frozen=True)
class GitCommit:
    sha: str
    subject: str


def run_git(repo_root: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.rstrip("\n")


def get_commits_since(repo_root: Path, since: str) -> list[GitCommit]:
    output = run_git(
        repo_root,
        ["log", f"--since={since}", "--pretty=format:%h%x09%s"],
    )

    if not output:
        return []

    commits = []
    for line in output.splitlines():
        sha, subject = line.split("\t", maxsplit=1)
        commits.append(GitCommit(sha=sha, subject=subject))

    return commits


def get_changed_files(repo_root: Path, since: str) -> list[str]:
    commit_range = run_git(
        repo_root,
        ["log", f"--since={since}", "--pretty=format:%H"],
    ).splitlines()

    if not commit_range:
        return []

    files = set()
    for commit in commit_range:
        output = run_git(
            repo_root,
            ["show", "--pretty=format:", "--name-only", commit],
        )
        files.update(line for line in output.splitlines() if line)

    return sorted(files)


def get_uncommitted_files(repo_root: Path) -> list[str]:
    output = run_git(repo_root, ["status", "--short"])
    if not output:
        return []

    files = []
    for line in output.splitlines():
        filename = line[3:].strip()
        if filename and filename != "faq.db":
            files.append(filename)

    return sorted(files)


def read_latest_learning_log_entry(repo_root: Path) -> str:
    path = repo_root / "docs" / "learning_log.md"
    if not path.exists():
        return ""

    text = path.read_text(encoding="utf-8")
    sections = text.split("\n## ")

    if len(sections) < 2:
        return ""

    latest = "## " + sections[1].strip()
    return latest


def build_post(
    commits: list[GitCommit],
    changed_files: list[str],
    uncommitted_files: list[str],
    latest_log_entry: str,
    post_date: date,
    hashtags: list[str],
) -> str:
    commit_lines = "\n".join(f"- `{commit.sha}` {commit.subject}" for commit in commits)
    file_lines = "\n".join(f"- `{filename}`" for filename in changed_files[:8])
    hashtag_line = " ".join(hashtags)

    if not commit_lines:
        commit_lines = "- No commits found in the selected window."

    if not file_lines:
        file_lines = "- No changed files found in the selected window."

    uncommitted_lines = "\n".join(f"- `{filename}`" for filename in uncommitted_files)
    if not uncommitted_lines:
        uncommitted_lines = "- No uncommitted files to review."

    return f"""# LinkedIn Draft - {post_date.isoformat()}

Today in {hashtags[0]}, I continued building my LLM Zoomcamp learning project.

LinkedIn profile: {LINKEDIN_PROFILE_URL}

## Progress

{commit_lines}

## Repo Artifacts

{file_lines}

## Uncommitted Files to Review

{uncommitted_lines}

## Reflection

{summarize_log_entry(latest_log_entry)}

## LinkedIn Post

Today in {hashtags[0]}, I made progress on my LLM Zoomcamp learning project.

What I worked on:
{commit_lines}

The useful learning point today was connecting the code changes to clear documentation and reproducible notebooks. This makes the project easier to revisit, explain, and share publicly.

Repo: https://github.com/waigisteve/llm-zoomcamp-2026-codesteve

{hashtag_line}

## Submission Checklist

- [ ] Review and edit the post manually.
- [ ] Publish on LinkedIn.
- [ ] Submit the published post link through the course platform.
- [ ] Update `docs/learning_in_public.md` with the public link and moderation status.
"""


def summarize_log_entry(entry: str) -> str:
    if not entry:
        return "No learning-log entry found yet. Add one to `docs/learning_log.md` before publishing."

    lines = []
    for line in entry.splitlines():
        if line.startswith("## ") or line.startswith("- "):
            lines.append(line)
        if len(lines) >= 8:
            break

    return "\n".join(lines)


def write_post(repo_root: Path, content: str, post_date: date) -> Path:
    output_dir = repo_root / "docs" / "public_posts"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{post_date.isoformat()}-linkedin.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a daily LinkedIn learning-in-public draft from repo progress.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to the repository root.",
    )
    parser.add_argument(
        "--since",
        default=DEFAULT_SINCE,
        help="Git log window, for example 'yesterday 21:00', 'midnight', or '2026-06-10 21:00'.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Post date in YYYY-MM-DD format.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    post_date = datetime.strptime(args.date, "%Y-%m-%d").date()

    commits = get_commits_since(repo_root, args.since)
    changed_files = get_changed_files(repo_root, args.since)
    uncommitted_files = get_uncommitted_files(repo_root)
    latest_log_entry = read_latest_learning_log_entry(repo_root)
    content = build_post(
        commits=commits,
        changed_files=changed_files,
        uncommitted_files=uncommitted_files,
        latest_log_entry=latest_log_entry,
        post_date=post_date,
        hashtags=DEFAULT_HASHTAGS,
    )

    output_path = write_post(repo_root, content, post_date)
    print(output_path)


if __name__ == "__main__":
    main()
