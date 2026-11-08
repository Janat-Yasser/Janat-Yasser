# Copyright (c) 2026 Janat Yasser. All rights reserved.
"""
Rewrites the "Lab log" in README.md from my latest public commits.

    GITHUB_TOKEN=... python scripts/update_log.py           (what the Action runs)
    python scripts/update_log.py --commits commits.json    (offline: a saved list of {repo, date, message})

Takes my most recently pushed public repositories (not this one, not forks),
reads their latest commits, skips merges, and lists the newest commit messages
(first line only) across all of them. The README changes only between
<!-- LOG:START --> and <!-- LOG:END -->.

It uses the repository and commit endpoints rather than the Events API,
whose push events no longer list commits.
"""
import argparse
import json
import os
import re
import urllib.request
from datetime import datetime
from pathlib import Path

USER = "Janat-Yasser"
README = Path(__file__).resolve().parent.parent / "README.md"
MAX_LINES = 6


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-lab-log"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch(n_repos=6):
    repos = [r for r in api(f"/users/{USER}/repos?sort=pushed&per_page=30&type=owner")
             if not r["fork"] and not r["private"] and r["name"].lower() != USER.lower()][:n_repos]
    out = []
    for r in repos:
        for c in api(f"/repos/{USER}/{r['name']}/commits?per_page=5"):
            out.append({"repo": r["name"], "date": c["commit"]["author"]["date"], "message": c["commit"]["message"]})
    return out


def lines(commits):
    out, seen = [], set()
    for c in sorted(commits, key=lambda c: c["date"], reverse=True):
        repo, msg = c["repo"], c["message"].splitlines()[0].strip()
        if not msg or msg.lower().startswith("merge") or (repo, msg) in seen:
            continue
        seen.add((repo, msg))
        day = datetime.strptime(c["date"][:10], "%Y-%m-%d").strftime("%b %d")
        msg = msg.replace("|", "/").replace("<", "&lt;")
        out.append(f"`{day}` &nbsp;**[{repo}](https://github.com/{USER}/{repo})** &nbsp;{msg}<br>")
        if len(out) == MAX_LINES:
            break
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--commits", help="read commits from this JSON file instead of the API")
    a = p.parse_args()
    commits = json.loads(Path(a.commits).read_text()) if a.commits else fetch()
    body = "\n".join(lines(commits)) or "<sub>Nothing public this week. Probably training something.</sub>"
    text = README.read_text(encoding="utf-8")
    new = re.sub(r"(<!-- LOG:START -->\n).*?(\n?<!-- LOG:END -->)", lambda m: m.group(1) + body + "\n" + m.group(2).lstrip("\n"),
                 text, flags=re.S)
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("log updated")
    else:
        print("log unchanged")


if __name__ == "__main__":
    main()
