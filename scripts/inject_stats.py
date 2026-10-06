#!/usr/bin/env python3
"""
inject_stats.py — Fetches live GitHub stats and injects them into SVG templates.

Usage:
    python scripts/inject_stats.py

Environment Variables:
    GITHUB_USERNAME  — Target GitHub username (default: ommprakashmohanty)
    GITHUB_TOKEN     — Personal access token for higher API rate limits (optional)

The script reads all .svg files in assets/, finds placeholder patterns
like {{STARS}}, {{REPOS}}, {{FOLLOWERS}}, and replaces them with live
values fetched from the GitHub REST API. On subsequent runs, previously
injected numeric values are also detected and updated.
"""

import os
import re
import json
import urllib.request
import urllib.error
import sys

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "ommprakashmohanty")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


def github_api(endpoint: str) -> dict | list:
    """Make an authenticated GET request to the GitHub REST API."""
    url = f"https://api.github.com{endpoint}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "github-profile-stats-injector")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[ERROR] GitHub API returned {e.code} for {endpoint}: {e.reason}")
        sys.exit(1)


def fetch_stats() -> dict:
    """Fetch user-level stats: public repos, followers, and total stars."""
    user = github_api(f"/users/{GITHUB_USERNAME}")
    repos_count = user.get("public_repos", 0)
    followers = user.get("followers", 0)

    # Paginate through all repos to sum stargazers
    total_stars = 0
    page = 1
    while True:
        repos = github_api(
            f"/users/{GITHUB_USERNAME}/repos?per_page=100&page={page}&sort=updated"
        )
        if not repos:
            break
        for repo in repos:
            total_stars += repo.get("stargazers_count", 0)
        if len(repos) < 100:
            break
        page += 1

    return {
        "STARS": str(total_stars),
        "REPOS": str(repos_count),
        "FOLLOWERS": str(followers),
    }


def inject_into_svgs(stats: dict) -> None:
    """
    Replace stat placeholders in all SVG files under assets/.

    Handles both the initial template form  {{KEY}}
    and previously-injected numeric form   <number>
    by matching the surrounding context text (e.g. '> Stars<').
    """
    # Build regex patterns that match either the placeholder or a previously
    # injected number, using the surrounding text as anchors.
    # Example: >{{STARS}} Stars<  or  >42 Stars<  →  >NEW_VALUE Stars<
    patterns = {
        "STARS": {
            "find": r">((?:\d+|\{\{STARS\}\})) stars<",
            "replace": ">{val} stars<",
        },
        "REPOS": {
            "find": r">((?:\d+|\{\{REPOS\}\})) repos<",
            "replace": ">{val} repos<",
        },
        "FOLLOWERS": {
            "find": r">((?:\d+|\{\{FOLLOWERS\}\})) followers<",
            "replace": ">{val} followers<",
        },
    }

    if not os.path.isdir(ASSETS_DIR):
        print(f"[ERROR] Assets directory not found: {ASSETS_DIR}")
        sys.exit(1)

    for filename in sorted(os.listdir(ASSETS_DIR)):
        if not filename.endswith(".svg"):
            continue

        filepath = os.path.join(ASSETS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        modified = False
        for key, value in stats.items():
            pat = patterns.get(key)
            if not pat:
                continue
            new_content, count = re.subn(
                pat["find"],
                pat["replace"].format(val=value),
                content,
            )
            if count > 0:
                content = new_content
                modified = True
                print(f"  [{filename}] {key} → {value} ({count} replacement(s))")

        if modified:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ Updated {filename}")
        else:
            print(f"  — {filename}: no placeholders found, skipped.")


def main():
    print(f"[*] Fetching GitHub stats for @{GITHUB_USERNAME}...")
    stats = fetch_stats()
    print(f"[*] Stats: {stats}")
    print(f"[*] Injecting into SVGs in {ASSETS_DIR}...")
    inject_into_svgs(stats)
    print("[✓] Done.")


if __name__ == "__main__":
    main()
