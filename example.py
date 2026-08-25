"""Minimal LinkedIn profile API call — one typed row per profile.

Docs & schema: https://quanticdata.io/collectors/linkedin-profile-scraper-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/linkedin_profile/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "profiles": [
            "williamhgates"
        ],
        "max_results": 5
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("name"), row.get("headline"), row.get("location"))
print(f"{len(data['results'])} profiles, cost ${data['cost']}")
