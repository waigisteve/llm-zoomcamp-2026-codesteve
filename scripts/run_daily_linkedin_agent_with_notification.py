from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENT_SCRIPT = REPO_ROOT / "scripts" / "daily_linkedin_agent.py"


def run_agent(post_date: str | None) -> Path:
    command = [str(REPO_ROOT / ".venv" / "bin" / "python"), str(AGENT_SCRIPT)]

    if post_date:
        command.extend(["--date", post_date])

    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    output = result.stdout.strip().splitlines()
    if not output:
        raise RuntimeError("Daily LinkedIn agent did not print an output path.")

    return Path(output[-1])


def notify_windows(draft_path: Path) -> None:
    windows_path = to_windows_path(draft_path)
    title = "LinkedIn draft ready"
    message = f"Review your learning-in-public draft: {windows_path}"

    script = f"""
Add-Type -AssemblyName System.Windows.Forms
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.BalloonTipTitle = {powershell_string(title)}
$notify.BalloonTipText = {powershell_string(message)}
$notify.Visible = $true
$notify.ShowBalloonTip(10000)
Start-Sleep -Seconds 12
$notify.Dispose()
"""

    subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        check=True,
        capture_output=True,
        text=True,
    )


def to_windows_path(path: Path) -> str:
    result = subprocess.run(
        ["wslpath", "-w", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def powershell_string(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the daily LinkedIn agent and show a Windows notification.",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Post date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--no-notify",
        action="store_true",
        help="Generate the draft without sending the Windows notification.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    draft_path = run_agent(args.date)

    if not args.no_notify:
        notify_windows(draft_path)

    print(draft_path)


if __name__ == "__main__":
    main()
