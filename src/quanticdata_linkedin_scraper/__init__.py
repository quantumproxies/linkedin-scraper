"""LinkedIn Scraper: LinkedIn scraper for Python and the command line: public profiles, company pages and job listings for a role and location, as JSON or CSV. Free and open source; sign in with your QuanticData account, no LinkedIn login, proxies or headless browser to run.

    from quanticdata_linkedin_scraper import LinkedInScraper

    scraper = LinkedInScraper()   # saved login (`linkedin-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.profiles(...)   # public LinkedIn profiles by slug or /in/ URL
    run = scraper.companies(...)   # public LinkedIn company pages by slug or /company/ URL
    run = scraper.jobs(...)   # public LinkedIn job listings for a role and location
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["LinkedInScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class LinkedInScraper:
    """LinkedIn Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="linkedin-scraper/0.1.0 (+https://github.com/quantumproxies/linkedin-scraper)", timeout=timeout)

    def profiles(
        self, profiles: Union[str, Sequence[str]],
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Public LinkedIn profile preview — name, headline, company, location.

        Args:
            profiles: Profile slugs (williamhgates) or /in/ URLs, one per line.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many profiles to deliver at most (1–50). You pay only for delivered profiles.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per profile: see ``types.LinkedinProfileRow``.
        """
        payload = {
            "profiles": _as_list(profiles),
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("linkedin_profile", payload, wait=wait, timeout=timeout)

    def companies(
        self, companies: Union[str, Sequence[str]],
        *,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Public LinkedIn company page — employees, followers, industry, HQ.

        Args:
            companies: Company slugs (microsoft) or /company/ URLs, one per line.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many companies to deliver at most (1–50). You pay only for delivered companies.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per company: see ``types.LinkedinCompanyRow``.
        """
        payload = {
            "companies": _as_list(companies),
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("linkedin_company", payload, wait=wait, timeout=timeout)

    def jobs(
        self, query: str,
        *,
        location: Optional[str] = None,
        remote_only: Optional[bool] = None,
        posted_within_days: Optional[int] = None,
        include_details: Optional[bool] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Public LinkedIn job listings for a role and location.

        Args:
            query: Job title or keywords, e.g. "data engineer".
            location: City, region or country, e.g. "New York" or "Italy".
            remote_only: Only listings LinkedIn marks as remote.
            posted_within_days: Only listings posted in the last N days (1–30).
            include_details: Also read each job's public posting: full description, seniority level, employment type, job function, industries and applicant count. One extra request per job, so runs take longer; off by default.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many jobs to deliver at most (1–300). You pay only for delivered jobs.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 300 rows, one per job: see ``types.LinkedinJobsRow``.
        """
        payload = {
            "query": query,
            "location": location,
            "remote_only": remote_only,
            "posted_within_days": posted_within_days,
            "include_details": include_details,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("linkedin_jobs", payload, wait=wait, timeout=timeout)
