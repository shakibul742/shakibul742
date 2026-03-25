import requests
import datetime
import os

USERNAME = "shakibul742"
TOKEN = os.getenv('GH_TOKEN')
headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

def get_total_active_days():
    user_info = requests.get(f"https://api.github.com/users/{USERNAME}").json()
    start_year = int(user_info.get("created_at", "2020")[:4])
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
    badge_url = f"https://img.shields.io/badge/Total_Active_Days-{active_days}-7aa2f7?style=flat-square&labelColor=1f2335&logo=github"
    
    readme_content = f"""---

# 👨‍💻 About Me

Cybersecurity student focused on **Security Operations, Threat Detection, Log Analysis, and Digital Forensics**.

I develop defensive security expertise through **hands-on cyber defense labs, threat analysis, and real-world security simulation platforms**.

My long-term goal is to work as a **Security Operations Center (SOC) Analyst**, protecting systems through effective monitoring, investigation, and incident response.

---

# 🎯 Career Focus

🛡️ **Defensive Security** | ⚔️ **Offensive Knowledge** | 📊 **SIEM Monitoring** | 🔍 **Threat Hunting**

* Security Operations Center (SOC) Analyst
* Threat Detection & Incident Response
* SIEM Monitoring & Log Analysis
* Digital Forensics Investigation
* Network Security Monitoring

---

# 🛠 Technical Skills

### 🖥 Computer & Operating System Fundamentals

<p>
<img src="https://skillicons.dev/icons?i=windows,linux,ubuntu,debian,fedora,kali" height="42"/>
<img src="https://img.shields.io/badge/Desktop-GNOME-4A86CF?style=flat-square&logo=gnome"/>
<img src="https://img.shields.io/badge/Desktop-KDE-1D99F3?style=flat-square&logo=kde"/>
<img src="https://img.shields.io/badge/Desktop-XFCE-2284F2?style=flat-square"/>
</p>

* Computer Systems Fundamentals
* Linux & Windows Administration Basics
* Multi-distribution Linux Experience

*(Windows, Ubuntu, Debian, Fedora, Linux Mint, Kali Linux — GNOME • KDE • XFCE environments)*

---

### 🌐 Networking & Cybersecurity

* Networking Fundamentals (TCP/IP, DNS, HTTP)
* Routing & Switching Basics
* Cybersecurity Core Principles
* Red Teaming Fundamentals (Attacker Perspective)

---

### 💻 Programming & Scripting

<p>
<img src="https://skillicons.dev/icons?i=c,cpp,python,java,bash,dart" height="42"/>
</p>

C • C++ • Python • Java • Bash • Dart

---

# 🧪 Security Practice Platforms

<p align="center">

<a href="https://tryhackme.com/p/shakibul742" target="_blank">
<img src="https://img.shields.io/badge/TryHackMe-Top%2015%25-212121?style=for-the-badge&logo=tryhackme&logoColor=red"/>
</a>

<a href="https://app.letsdefend.io/user/shakibul742" target="_blank">
<img src="https://img.shields.io/badge/LetsDefend-BD%20Rank%2027-00A8FF?style=for-the-badge&logo=shield&logoColor=white"/>
</a>

</p>

* Blue Team Practical Labs
* Detection Engineering Challenges
* Incident Response Simulations

---

# 📚 Currently Learning

<p>
<img src="https://img.shields.io/badge/Digital_Forensics-Learning-blue?style=flat-square"/>
<img src="https://img.shields.io/badge/SIEM-Splunk%20%2F%20Wazuh-blue?style=flat-square"/>
<img src="https://img.shields.io/badge/Windows-Log%20Analysis-blue?style=flat-square"/>
<img src="https://img.shields.io/badge/SOC-Alert%20Investigation-blue?style=flat-square"/>
</p>

* Digital Forensics
* SIEM Platforms (Splunk / Wazuh)
* Windows Log Analysis
* SOC Alert Investigation
* Blue Team Incident Handling

---

# 📊 GitHub Activity

<p align="center">
  <img src="{badge_url}" alt="Total Active Days" />
</p>

<p align="center">
<img src="https://github-readme-streak-stats.herokuapp.com/?user=shakibul742&theme=tokyonight&hide_border=true" height="165"/>
</p>

<p align="center">
<img src="https://github-readme-activity-graph.vercel.app/graph?username=shakibul742&theme=tokyo-night&hide_border=true"/>
</p>

---

# 📫 Contact

🎓 Academic Email <a href="mailto:shakibul.240112@s.pust.ac.bd" target="_blank">
[shakibul.240112@s.pust.ac.bd](mailto:shakibul.240112@s.pust.ac.bd) </a>

📧 Personal Email <a href="mailto:shakibul74254285@gmail.com" target="_blank">
[shakibul74254285@gmail.com](mailto:shakibul74254285@gmail.com) </a>

💼 LinkedIn <a href="https://www.linkedin.com/in/shakibul742/" target="_blank">
linkedin.com/in/shakibul742 </a>

📘 Facebook <a href="https://www.facebook.com/shakibul742.cse.pust" target="_blank">
facebook.com/shakibul742.cse.pust </a>

---

<p align="center">
  <img src="https://github.com/shakibul742/shakibul742/blob/output/github-contribution-grid-snake-dark.svg" alt="Contribution Snake" />
</p>

<p align="center">
  <sub>Tracking contribution patterns with an animated activity stream.</sub>
</p>
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("README fixed and updated successfully.")

if __name__ == "__main__":
    days = get_total_active_days()
    print(f"Total Active Days: {days}")
    update_readme(days)
