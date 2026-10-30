# LinkedIn Scraper

[![ci](https://github.com/quantumproxies/linkedin-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/linkedin-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape LinkedIn from Python or the command line: public profiles, company pages, and job listings for a role and a location, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API and reads public pages only, so there is no LinkedIn login to share, no proxy to rotate and no headless browser to keep alive: sign in to QuanticData once and run a command. The same collectors work from Claude or any MCP client, and from n8n.

```bash
pip install git+https://github.com/quantumproxies/linkedin-scraper
linkedin-scraper login
linkedin-scraper jobs "data engineer" --location "United States" --posted-within-days 7 --max-results 100 -o jobs.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=linkedin-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `linkedin-scraper profiles` | profile slugs or /in/ URLs | Name, headline, company, location, 13 fields per row ([fields and price](https://quanticdata.io/collectors/linkedin-profile-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=linkedin-scraper)) | up to 50 |
| `linkedin-scraper companies` | company slugs or /company/ URLs | Employees, followers, industry, HQ, 19 fields per row ([fields and price](https://quanticdata.io/collectors/linkedin-company-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=linkedin-scraper)) | up to 50 |
| `linkedin-scraper jobs` | role, optional location | Public LinkedIn job listings for a role and location, 19 fields per row ([fields and price](https://quanticdata.io/collectors/linkedin-jobs-api/?utm_source=github&utm_medium=readme&utm_campaign=linkedin-scraper)) | up to 300 |

`jobs` narrows the listings with `--location` (a city, region or country), `--remote-only` and `--posted-within-days` (1 to 30). `--include-details` also opens each posting for the full description, seniority level, employment type, job function, industries and applicant count.

## Sample output

A real row from `linkedin-scraper profiles williamhgates --max-results 1` (2026-10-22):

```json
{
  "url": "https://www.linkedin.com/in/williamhgates",
  "name": "Bill Gates",
  "slug": "williamhgates",
  "image": "https://media.licdn.com/dms/image/v2/D5603AQF-RYZP55jmXA/profile-displayphoto-shrink_200_200/B56ZRi8g.aGsAY-/0/1736826818802?e=2147483647&v=beta&t=bKWfN6UwwtiCqFWsG7rBELbd48qJOAMLdxhBzzkJV0k",
  "company": "Gates Foundation",
  "country": "US",
  "headline": "Chair, Gates Foundation and Founder, Breakthrough Energy",
  "location": "Seattle, Washington, United States",
  "education": [
    "Harvard University"
  ],
  "followers": 41000000,
  "job_titles": [
    "Co-chair",
    "Founder",
    "Co-founder"
  ],
  "company_url": "https://www.linkedin.com/company/gates-foundation",
  "connections": 8
}
```

## Python

```python
from quanticdata_linkedin_scraper import LinkedInScraper

linkedin = LinkedInScraper()  # saved login, or QUANTICDATA_API_KEY

people = linkedin.profiles(["williamhgates"])
print(people.rows[0]["headline"], people.rows[0]["followers"])

companies = linkedin.companies(["microsoft", "openai"])
for c in companies:
    print(c["name"], c["industry"], c["employees"], c["headquarters"])

jobs = linkedin.jobs("data engineer", location="United States", posted_within_days=7, max_results=100)
for j in jobs:
    print(j["posted_at"], j["company"], j["location"], j["title"])
jobs.to_csv("data_engineer_jobs.csv")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Company list enrichment**: Read a CSV with a column of LinkedIn company slugs or URLs and add industry, size band, employee and follower counts, website, headquarters and founding year to every row. See [`examples/enrich_companies.py`](examples/enrich_companies.py).
- **Jobs by role and city**: Pull the listings for a few roles in a few locations, deduplicate them by job id and keep one CSV you can chart by employer and posting date. See [`examples/jobs_by_role_city.py`](examples/jobs_by_role_city.py).
- **Job-change alerts**: Check the public profiles of the people you already work with every week and log when their company, headline or location changes. See [`examples/profile_changes.py`](examples/profile_changes.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `linkedin-scraper run <id> -o out.csv` collects it later.

### `linkedin-scraper profiles`

Public LinkedIn profile preview — name, headline, company, location.

```
linkedin-scraper profiles PROFILES [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `PROFILES` | string[] |  | Profile slugs (williamhgates) or /in/ URLs, one per line. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `10` | How many profiles to deliver at most (1–50). You pay only for delivered profiles. |

### `linkedin-scraper companies`

Public LinkedIn company page — employees, followers, industry, HQ.

```
linkedin-scraper companies COMPANIES [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `COMPANIES` | string[] |  | Company slugs (microsoft) or /company/ URLs, one per line. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `10` | How many companies to deliver at most (1–50). You pay only for delivered companies. |

### `linkedin-scraper jobs`

Public LinkedIn job listings for a role and location.

```
linkedin-scraper jobs QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | Job title or keywords, e.g. "data engineer". |
| `--location` | string |  | City, region or country, e.g. "New York" or "Italy". |
| `--remote-only` | boolean | `False` | Only listings LinkedIn marks as remote. |
| `--posted-within-days` | integer |  | Only listings posted in the last N days (1–30). |
| `--include-details` | boolean | `False` | Also read each job's public posting: full description, seniority level, employment type, job function, industries and applicant count. One extra request per job, so runs take longer; off by default. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `25` | How many jobs to deliver at most (1–300). You pay only for delivered jobs. |

## Output fields

<details><summary><code>linkedin-scraper profiles</code>: 13 fields</summary>

| Field | Type | Description |
|---|---|---|
| `slug` | string | Profile slug. |
| `name` | string | Full name. |
| `headline` | string or null | Profile headline. |
| `location` | string or null | Location as published. |
| `country` | string or null | Country when exposed. |
| `job_titles` | string[] | Titles listed in the public schema block. |
| `company` | string or null | Current company. |
| `company_url` | string or null | Company LinkedIn URL. |
| `education` | string[] | Schools listed publicly. |
| `followers` | integer or null | Follower count. |
| `connections` | integer or null | Connection count as shown. |
| `image` | string or null | Profile photo URL. |
| `url` | string | Profile URL. |

</details>

<details><summary><code>linkedin-scraper companies</code>: 19 fields</summary>

| Field | Type | Description |
|---|---|---|
| `slug` | string | Company slug. |
| `name` | string | Company name. |
| `description` | string or null | About text (trimmed). |
| `website` | string or null | Company website, always as a full URL. |
| `industry` | string or null | Industry as shown. |
| `employees` | integer or null | Employee count published on the page. |
| `followers` | integer or null | LinkedIn follower count. |
| `street` | string or null | HQ street. |
| `city` | string or null | HQ city. |
| `region` | string or null | HQ region/state. |
| `postal_code` | string or null | HQ postal code. |
| `country` | string or null | HQ country. |
| `logo` | string or null | Logo URL. |
| `url` | string | Company page URL. |
| `company_size` | string or null | Size band as LinkedIn states it ("10,001+ employees"). |
| `company_type` | string or null | Public Company, Privately Held, Nonprofit… |
| `founded` | integer or null | Founding year when the page states one. |
| `specialties` | string[] | Specialties listed on the page. |
| `headquarters` | string or null | Headquarters line as shown ("Redmond, Washington"). |

</details>

<details><summary><code>linkedin-scraper jobs</code>: 19 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position across pages. |
| `title` | string | Job title. |
| `company` | string or null | Employer. |
| `company_url` | string or null | Employer's LinkedIn page. |
| `location` | string or null | Location as shown. |
| `posted_at` | string or null | Posting date (ISO, from the card's &lt;time&gt;). |
| `posted_label` | string or null | Posting age as shown ("2 weeks ago"). |
| `salary` | string or null | Salary chip when LinkedIn shows one. |
| `benefits` | string or null | Status chip on the card when shown ("Actively Hiring", "Be an early applicant"). |
| `job_id` | string or null | LinkedIn job id (dedupe key). |
| `link` | string or null | Listing URL. |
| `logo` | string or null | Company logo URL. |
| `description` | string or null | With include_details: the full posting text. |
| `seniority` | string or null | With include_details: seniority level (Entry level, Mid-Senior level…). |
| `employment_type` | string or null | With include_details: Full-time, Part-time, Contract… |
| `job_function` | string or null | With include_details: job function as LinkedIn classifies it. |
| `industries` | string[] or null | With include_details: the employer's industries. |
| `applicants` | integer or null | With include_details: applicant count as a number (200 for "Over 200 applicants"). |
| `applicants_label` | string or null | With include_details: applicant count as shown. |

</details>

## Sign-in and API keys

- `linkedin-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `linkedin-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `linkedin-scraper login --api-key`.
- `linkedin-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=linkedin-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/linkedin_profile/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"profiles": ["williamhgates"], "max_results": 1}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=linkedin-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=linkedin-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this LinkedIn scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send profile or company slugs, or a role and a location, and get rows back; the requests run on QuanticData's side.

**Does it need my LinkedIn account?**

No. It reads public LinkedIn pages only, the ones anyone can open without signing in, and never asks for your LinkedIn login or cookies. You are responsible for respecting LinkedIn's terms and the data-protection rules that apply to how you use the data.

**How many results can one run return?**

Up to 50 profiles, 50 companies or 300 job listings per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Lists such as job titles, schools and specialties are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/profile_changes.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Google Maps Scraper](https://github.com/quantumproxies/google-maps-scraper): Google Maps scraper for Python and the command line.
- [Instagram Scraper](https://github.com/quantumproxies/instagram-scraper): Instagram scraper for Python and the command line.
- [Reddit Scraper](https://github.com/quantumproxies/reddit-scraper): Reddit scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=linkedin-scraper).
