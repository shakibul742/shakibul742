import datetime
import html
import os
import time
from pathlib import Path

import requests


USERNAME = "shakibul742"
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
} if TOKEN else {"Accept": "application/vnd.github+json"}
ASSET_PATH = Path("assets/github-activity.svg")
API_TIMEOUT_SECONDS = 30
MAX_ATTEMPTS = 3

CONTRIBUTIONS_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays { date contributionCount }
        }
      }
    }
  }
}
"""


def request_with_retries(method, url, **kwargs):
    """Retry transient GitHub failures without replacing the current dashboard."""
    last_error = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            response = requests.request(
                method, url, headers=HEADERS, timeout=API_TIMEOUT_SECONDS, **kwargs
            )
            if response.status_code in {429, 500, 502, 503, 504}:
                response.raise_for_status()
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            last_error = error
            if attempt == MAX_ATTEMPTS - 1:
                break
            time.sleep(2**attempt)
    raise RuntimeError(f"GitHub request failed after {MAX_ATTEMPTS} attempts: {last_error}")


def get_contribution_days():
    if not TOKEN:
        raise RuntimeError("GH_TOKEN is required to refresh contribution statistics.")

    user_response = request_with_retries("GET", f"https://api.github.com/users/{USERNAME}")
    start_year = int(user_response.json()["created_at"][:4])
    current_year = datetime.datetime.now(datetime.UTC).year
    contribution_days = {}

    for year in range(start_year, current_year + 1):
        response = request_with_retries(
            "POST",
            "https://api.github.com/graphql",
            json={
                "query": CONTRIBUTIONS_QUERY,
                "variables": {
                    "login": USERNAME,
                    "from": f"{year}-01-01T00:00:00Z",
                    "to": f"{year}-12-31T23:59:59Z",
                },
            },
        )
        payload = response.json()
        if payload.get("errors"):
            raise RuntimeError(payload["errors"])

        weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        for week in weeks:
            for day in week["contributionDays"]:
                contribution_days[day["date"]] = day["contributionCount"]

    return contribution_days


def streaks(contribution_days, today):
    active_dates = sorted(
        parsed_date
        for date, count in contribution_days.items()
        for parsed_date in [datetime.date.fromisoformat(date)]
        if count > 0 and parsed_date <= today
    )
    if not active_dates:
        return 0, 0, 0

    longest = run = 1
    for previous, current in zip(active_dates, active_dates[1:]):
        run = run + 1 if current == previous + datetime.timedelta(days=1) else 1
        longest = max(longest, run)

    active_lookup = set(active_dates)
    current = 0
    cursor = today
    # A streak remains active when the last contribution was yesterday.
    if cursor not in active_lookup:
        cursor -= datetime.timedelta(days=1)
    while cursor in active_lookup:
        current += 1
        cursor -= datetime.timedelta(days=1)
    return len(active_dates), current, longest


def heatmap_cells(contribution_days, today):
    start = today - datetime.timedelta(days=83)
    start -= datetime.timedelta(days=start.weekday())
    cells = []
    for offset in range(84):
        date = start + datetime.timedelta(days=offset)
        count = contribution_days.get(date.isoformat(), 0) if date <= today else 0
        level = 0 if count == 0 else min(4, 1 + int(count >= 3) + int(count >= 6) + int(count >= 10))
        cells.append((offset // 7, offset % 7, level))
    return cells


def render_dashboard(total, current, longest, cells, updated_at):
    colors = ["#1d2633", "#163e45", "#16746f", "#23bfa2", "#8ef0c4"]
    squares = "".join(
        f'<rect x="{532 + week * 24}" y="{111 + weekday * 17}" width="12" height="12" rx="3" fill="{colors[level]}" />'
        for week, weekday, level in cells
    )
    safe_updated_at = html.escape(updated_at)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="260" viewBox="0 0 900 260" role="img" aria-labelledby="title description">
  <title id="title">GitHub activity dashboard for {USERNAME}</title>
  <desc id="description">Current streak: {current} days. Longest streak: {longest} days. Total active days: {total}.</desc>
  <defs>
    <linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111c2d"/><stop offset="1" stop-color="#0b111d"/></linearGradient>
    <linearGradient id="accent" x1="0" x2="1"><stop stop-color="#42e8b5"/><stop offset="1" stop-color="#62a7ff"/></linearGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="900" height="260" rx="22" fill="#080d16"/>
  <rect x="1" y="1" width="898" height="258" rx="21" fill="url(#surface)" stroke="#27364b"/>
  <rect x="32" y="34" width="6" height="40" rx="3" fill="url(#accent)" filter="url(#glow)"/>
  <text x="54" y="49" fill="#dce9fa" font-family="Arial, Helvetica, sans-serif" font-size="13" font-weight="700" letter-spacing="2.5">GITHUB ACTIVITY</text>
  <text x="54" y="69" fill="#7f96b2" font-family="Arial, Helvetica, sans-serif" font-size="12">Reliable local snapshot • refreshed by GitHub Actions</text>
  <line x1="32" y1="94" x2="500" y2="94" stroke="#25344a"/>
  <text x="32" y="124" fill="#7f96b2" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700" letter-spacing="1.4">CURRENT STREAK</text>
  <text x="32" y="166" fill="#8ef0c4" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="700">{current}<tspan font-size="15" fill="#7f96b2"> days</tspan></text>
  <text x="205" y="124" fill="#7f96b2" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700" letter-spacing="1.4">LONGEST STREAK</text>
  <text x="205" y="166" fill="#dce9fa" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="700">{longest}<tspan font-size="15" fill="#7f96b2"> days</tspan></text>
  <text x="378" y="124" fill="#7f96b2" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700" letter-spacing="1.4">ACTIVE DAYS</text>
  <text x="378" y="166" fill="#dce9fa" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="700">{total}</text>
  <text x="532" y="82" fill="#7f96b2" font-family="Arial, Helvetica, sans-serif" font-size="11" font-weight="700" letter-spacing="1.4">LAST 12 WEEKS</text>
  {squares}
  <circle cx="40" cy="216" r="4" fill="#8ef0c4"/>
  <text x="52" y="220" fill="#a4b6cb" font-family="Arial, Helvetica, sans-serif" font-size="12">Last successful refresh: {safe_updated_at} UTC</text>
  <text x="836" y="220" fill="#526984" font-family="Arial, Helvetica, sans-serif" font-size="11" text-anchor="end">{USERNAME}</text>
</svg>'''


def write_dashboard(contribution_days):
    today = datetime.datetime.now(datetime.UTC).date()
    total, current, longest = streaks(contribution_days, today)
    dashboard = render_dashboard(
        total, current, longest, heatmap_cells(contribution_days, today), today.isoformat()
    )
    ASSET_PATH.write_text(dashboard, encoding="utf-8")
    print(f"Updated activity dashboard: {total} active days, {current}-day streak")


if __name__ == "__main__":
    write_dashboard(get_contribution_days())
