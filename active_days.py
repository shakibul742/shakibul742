import requests
import datetime
import os
import re

USERNAME = "shakibul742"
TOKEN = os.getenv('GH_TOKEN')
headers = {"Authorization": f"Bearer {TOKEN}"}

def get_total_active_days():
    user_info = requests.get(f"https://api.github.com/users/{USERNAME}").json()
    start_year = int(user_info.get("created_at")[:4])
    current_year = datetime.datetime.now().year
    total_active_days = 0

    for year in range(start_year, current_year + 1):
        query = """
        query {
          user(login: "%s") {
            contributionsCollection(from: "%s-01-01T00:00:00Z", to: "%s-12-31T23:59:59Z") {
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
        """ % (USERNAME, year, year)
        
        response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers).json()
        
        try:
            weeks = response['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
            for week in weeks:
                for day in week['contributionDays']:
                    if day['contributionCount'] > 0:
                        total_active_days += 1
        except Exception as e:
            print(f"Error fetching data for {year}: {e}")

    return total_active_days

def update_readme(active_days):
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()

    badge_url = f"https://img.shields.io/badge/Total_Active_Days-{active_days}-7aa2f7?style=flat-square&labelColor=1f2335&logo=github"
    markdown_badge = f"![Active Days]({badge_url})"
    
    start_tag = ''
    end_tag = ''

    # Safety Check: Only update if tags exist
    if start_tag in readme and end_tag in readme:
        updated_readme = re.sub(
            f'{start_tag}.*?{end_tag}',
            f'{start_tag}\n<p align="center">\n  {markdown_badge}\n</p>\n{end_tag}',
            readme,
            flags=re.DOTALL
        )
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(updated_readme)
        print("README updated successfully.")
    else:
        print("Error: Tags not found in README.md. File was not updated to prevent data loss.")

if __name__ == "__main__":
    days = get_total_active_days()
    print(f"Total Active Days: {days}")
    update_readme(days)
