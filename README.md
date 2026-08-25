# LinkedIn profile API — examples

Public LinkedIn profile preview — name, headline, company, location.

**Live page, full schema & pricing → [quanticdata.io/collectors/linkedin-profile-scraper-api/](https://quanticdata.io/collectors/linkedin-profile-scraper-api/)**

Reads the LOGGED-OUT LinkedIn profile page for a list of slugs or URLs and delivers name, headline, location, current company, job titles, education, follower and connection counts and the profile photo. Only what LinkedIn publishes to visitors: the fields behind its sign-in wall (full experience history, contact details) are not collected and never guessed. No login, no cookies, no browser.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/linkedin_profile/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"profiles": ["williamhgates"], "max_results": 5}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `profiles` (array, required) — Profile slugs (williamhgates) or /in/ URLs, one per line.
- `country` (string) — ISO 3166-1 alpha-2 code — proxy exit geo and Google locale (gl). Omit for the default pool.
- `max_results` (integer) — How many profiles to deliver at most (1–50). You pay only for delivered profiles.

## Output — one row per profile

| field | type | description |
|---|---|---|
| `slug` | string | Profile slug. |
| `name` | string | Full name. |
| `headline` | string | Profile headline. |
| `location` | string | Location as published. |
| `country` | string | Country when exposed. |
| `job_titles` | string[] | Titles listed in the public schema block. |
| `company` | string | Current company. |
| `company_url` | string | Company LinkedIn URL. |
| `education` | string[] | Schools listed publicly. |
| `followers` | integer | Follower count. |
| `connections` | integer | Connection count as shown. |
| `image` | string | Profile photo URL. |
…and 1 more fields — full schema on the [live page](https://quanticdata.io/collectors/linkedin-profile-scraper-api/).

## Pricing

**$0.005 per delivered profile** ($5 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 400 profiles — no card required.

## Links

- This collector: https://quanticdata.io/collectors/linkedin-profile-scraper-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
