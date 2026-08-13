import datetime
import os
import re
from pathlib import Path

import requests


USERNAME = "shakibul742"
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
README_PATH = Path("README.md")
ACTIVE_DAYS_PATTERN = re.compile(
    r"<!-- ACTIVE_DAYS:START -->.*?<!-- ACTIVE_DAYS:END -->", re.DOTALL
)


def get_total_active_days():
    user_response = requests.get(
        f"https://api.github.com/users/{USERNAME}", headers=HEADERS, timeout=30
    )
    user_response.raise_for_status()
    start_year = int(user_response.json()["created_at"][:4])
    current_year = datetime.datetime.now(datetime.UTC).year
    total_active_days = 0

    for year in range(start_year, current_year + 1):
        query = """
        query($login: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $login) {
            contributionsCollection(from: $from, to: $to) {
              contributionCalendar {
                weeks {
                  contributionDays {
                    contributionCount
                  }
                }
              }
            }
          }
        }
        """
        response = requests.post(
            "https://api.github.com/graphql",
            json={
                "query": query,
                "variables": {
                    "login": USERNAME,
                    "from": f"{year}-01-01T00:00:00Z",
                    "to": f"{year}-12-31T23:59:59Z",
                },
            },
            headers=HEADERS,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("errors"):
            raise RuntimeError(payload["errors"])

        weeks = payload["data"]["user"]["contributionsCollection"][
            "contributionCalendar"
        ]["weeks"]
        total_active_days += sum(
            day["contributionCount"] > 0
            for week in weeks
            for day in week["contributionDays"]
        )

    return total_active_days


def update_readme(active_days):
    replacement = (
        "  <!-- ACTIVE_DAYS:START -->\n"
        f'  <img src="https://img.shields.io/badge/Total%20Active%20Days-{active_days}-3fb950?style=for-the-badge&logo=github&logoColor=white" alt="Total Active Days" />\n'
        "  <!-- ACTIVE_DAYS:END -->"
    )
    readme_content = README_PATH.read_text(encoding="utf-8")
    updated_content, replacements = ACTIVE_DAYS_PATTERN.subn(replacement, readme_content)

    if replacements != 1:
        raise RuntimeError("Expected exactly one active-days marker in README.md.")

    README_PATH.write_text(updated_content, encoding="utf-8")
    print(f"Updated active-days badge: {active_days}")


if __name__ == "__main__":
    days = get_total_active_days()
    update_readme(days)
