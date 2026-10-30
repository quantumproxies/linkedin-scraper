"""LinkedIn job listings for several roles in several locations, in one CSV.

    python jobs_by_role_city.py --roles "data engineer" "analytics engineer" --locations "New York" "Austin" --days 7

Listings are deduplicated by job id, and each keeps the role and location that
found it. Add --details to open every posting for the full description,
seniority, employment type and applicant count (one extra request per job, so
the run takes longer). At the end the employers with the most listings are
printed.
"""

import argparse
from collections import Counter

from quanticdata_linkedin_scraper import LinkedInScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--roles", nargs="+", required=True)
    parser.add_argument("--locations", nargs="+", required=True, help="cities, regions or countries")
    parser.add_argument("--days", type=int, help="only listings posted in the last N days (1-30)")
    parser.add_argument("--remote", action="store_true", help="only listings marked as remote")
    parser.add_argument("--details", action="store_true", help="open each posting for the full description")
    parser.add_argument("--per-search", type=int, default=50, help="listings per role and location (max 300)")
    parser.add_argument("--out", default="jobs.csv")
    args = parser.parse_args()

    linkedin = LinkedInScraper()
    jobs = {}
    for role in args.roles:
        for location in args.locations:
            run = linkedin.jobs(role, location=location, posted_within_days=args.days, remote_only=args.remote,
                                include_details=args.details, max_results=args.per_search)
            for job in run:
                key = job.get("job_id") or job.get("link")
                jobs.setdefault(key, {"search_role": role, "search_location": location, **job})
            print(f"{role!r} in {location}: {len(run)} listings")

    rows = list(jobs.values())
    write(rows, args.out)
    print(f"{len(rows)} unique listings written to {args.out}")
    for company, count in Counter(r["company"] for r in rows if r.get("company")).most_common(10):
        print(f"  {count:4d}  {company}")


if __name__ == "__main__":
    main()
