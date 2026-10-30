"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class LinkedinProfileRow(TypedDict, total=False):
    """One row of `linkedin-scraper profiles` (linkedin_profile v1.0.2)."""

    slug: str
    """Profile slug."""
    name: str
    """Full name."""
    headline: Optional[str]
    """Profile headline."""
    location: Optional[str]
    """Location as published."""
    country: Optional[str]
    """Country when exposed."""
    job_titles: List[str]
    """Titles listed in the public schema block."""
    company: Optional[str]
    """Current company."""
    company_url: Optional[str]
    """Company LinkedIn URL."""
    education: List[str]
    """Schools listed publicly."""
    followers: Optional[int]
    """Follower count."""
    connections: Optional[int]
    """Connection count as shown."""
    image: Optional[str]
    """Profile photo URL."""
    url: str
    """Profile URL."""

class LinkedinCompanyRow(TypedDict, total=False):
    """One row of `linkedin-scraper companies` (linkedin_company v1.1.1)."""

    slug: str
    """Company slug."""
    name: str
    """Company name."""
    description: Optional[str]
    """About text (trimmed)."""
    website: Optional[str]
    """Company website, always as a full URL."""
    industry: Optional[str]
    """Industry as shown."""
    employees: Optional[int]
    """Employee count published on the page."""
    followers: Optional[int]
    """LinkedIn follower count."""
    street: Optional[str]
    """HQ street."""
    city: Optional[str]
    """HQ city."""
    region: Optional[str]
    """HQ region/state."""
    postal_code: Optional[str]
    """HQ postal code."""
    country: Optional[str]
    """HQ country."""
    logo: Optional[str]
    """Logo URL."""
    url: str
    """Company page URL."""
    company_size: Optional[str]
    """Size band as LinkedIn states it ("10,001+ employees")."""
    company_type: Optional[str]
    """Public Company, Privately Held, Nonprofit…"""
    founded: Optional[int]
    """Founding year when the page states one."""
    specialties: List[str]
    """Specialties listed on the page."""
    headquarters: Optional[str]
    """Headquarters line as shown ("Redmond, Washington")."""

class LinkedinJobsRow(TypedDict, total=False):
    """One row of `linkedin-scraper jobs` (linkedin_jobs v1.1.1)."""

    rank: int
    """1-based position across pages."""
    title: str
    """Job title."""
    company: Optional[str]
    """Employer."""
    company_url: Optional[str]
    """Employer's LinkedIn page."""
    location: Optional[str]
    """Location as shown."""
    posted_at: Optional[str]
    """Posting date (ISO, from the card's <time>)."""
    posted_label: Optional[str]
    """Posting age as shown ("2 weeks ago")."""
    salary: Optional[str]
    """Salary chip when LinkedIn shows one."""
    benefits: Optional[str]
    """Status chip on the card when shown ("Actively Hiring", "Be an early applicant")."""
    job_id: Optional[str]
    """LinkedIn job id (dedupe key)."""
    link: Optional[str]
    """Listing URL."""
    logo: Optional[str]
    """Company logo URL."""
    description: Optional[str]
    """With include_details: the full posting text."""
    seniority: Optional[str]
    """With include_details: seniority level (Entry level, Mid-Senior level…)."""
    employment_type: Optional[str]
    """With include_details: Full-time, Part-time, Contract…"""
    job_function: Optional[str]
    """With include_details: job function as LinkedIn classifies it."""
    industries: Optional[List[str]]
    """With include_details: the employer's industries."""
    applicants: Optional[int]
    """With include_details: applicant count as a number (200 for "Over 200 applicants")."""
    applicants_label: Optional[str]
    """With include_details: applicant count as shown."""
