"""Spot job changes in a list of public LinkedIn profiles.

Reads profiles.txt (one slug or /in/ URL per line), reads each public profile
and compares its current company, headline and location with the previous
run, kept in profiles_snapshot.json. Every change is printed and appended to
profile_changes.csv. Run it weekly from cron:

    0 7 * * 1  cd /path/to/here && python profile_changes.py

Needs a login (`linkedin-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import json
import os
from datetime import datetime, timezone

from quanticdata_linkedin_scraper import LinkedInScraper

WATCHED = ("company", "headline", "location")
CHANGE_FIELDS = ["checked_at", "slug", "name", "field", "before", "after", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--profiles", default="profiles.txt", help="file with one slug or /in/ URL per line")
    parser.add_argument("--snapshot", default="profiles_snapshot.json")
    parser.add_argument("--out", default="profile_changes.csv")
    args = parser.parse_args()

    with open(args.profiles, encoding="utf-8") as fh:
        wanted = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    previous = {}
    if os.path.exists(args.snapshot):
        with open(args.snapshot, encoding="utf-8") as fh:
            previous = json.load(fh)

    linkedin = LinkedInScraper()
    current = {}
    # The profile collector takes up to 50 profiles per run.
    for i in range(0, len(wanted), 50):
        for profile in linkedin.profiles(wanted[i:i + 50], max_results=50):
            current[profile["slug"]] = {k: profile.get(k) for k in ("name", "url") + WATCHED}

    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    changes = []
    for slug, now in current.items():
        before = previous.get(slug)
        if not before:
            continue
        for field in WATCHED:
            if before.get(field) != now.get(field):
                changes.append({"checked_at": checked_at, "slug": slug, "name": now.get("name"), "field": field,
                                "before": before.get(field), "after": now.get(field), "url": now.get("url")})

    new_file = not os.path.exists(args.out)
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CHANGE_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerows(changes)
    for change in changes:
        print(f"{change['name']}: {change['field']} {change['before']!r} -> {change['after']!r}")

    previous.update(current)
    with open(args.snapshot, "w", encoding="utf-8") as fh:
        json.dump(previous, fh, indent=1, ensure_ascii=False)
    print(f"{len(current)} profiles checked, {len(changes)} changes appended to {args.out}")


if __name__ == "__main__":
    main()
