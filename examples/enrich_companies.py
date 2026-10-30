"""Add LinkedIn company data to a CSV of companies.

    python enrich_companies.py accounts.csv --column linkedin --out accounts_enriched.csv

The input CSV needs a column with LinkedIn company slugs (microsoft) or
/company/ URLs. Every row keeps its own columns and gains industry, size band,
employee and follower counts, website, headquarters and founding year, each
prefixed with linkedin_. Rows with no matching page keep those columns empty.
"""

import argparse
import csv

from quanticdata_linkedin_scraper import LinkedInScraper, write

FIELDS = ["name", "industry", "company_size", "employees", "followers", "website", "headquarters", "founded", "url"]


def slug_of(value: str) -> str:
    value = value.strip().rstrip("/")
    if "/company/" in value:
        value = value.split("/company/", 1)[1].split("/")[0]
    return value.lower()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv_in", help="CSV with one company per row")
    parser.add_argument("--column", default="linkedin", help="column holding the slug or /company/ URL")
    parser.add_argument("--out", default="enriched.csv")
    args = parser.parse_args()

    with open(args.csv_in, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    slugs = sorted({slug_of(r[args.column]) for r in rows if (r.get(args.column) or "").strip()})

    linkedin = LinkedInScraper()
    found = {}
    # The company collector takes up to 50 companies per run.
    for i in range(0, len(slugs), 50):
        for company in linkedin.companies(slugs[i:i + 50], max_results=50):
            found[company["slug"].lower()] = company

    enriched = []
    for row in rows:
        company = found.get(slug_of(row.get(args.column) or ""), {})
        enriched.append({**row, **{f"linkedin_{k}": company.get(k) for k in FIELDS}})
    write(enriched, args.out)
    print(f"{len(found)} of {len(slugs)} companies matched, {len(enriched)} rows written to {args.out}")


if __name__ == "__main__":
    main()
