import requests
from collections import Counter
import os

USERNAME = os.getenv("GITLAB_USERNAME", "MARAST01")


GITLAB_USERNAME = "MARAST01"
GITLAB_TOKEN = ""  # se setea con GitHub Secrets

BASE_URL = "https://gitlab.com/api/v4"


def get_user():
    r = requests.get(f"{BASE_URL}/users?username={GITLAB_USERNAME}")
    r.raise_for_status()
    return r.json()[0]["id"]


def get_projects(user_id):
    projects = []
    page = 1

    while True:
        r = requests.get(
            f"{BASE_URL}/users/{user_id}/projects?per_page=100&page={page}",
            headers={"PRIVATE-TOKEN": GITLAB_TOKEN},
        )
        if not r.json():
            break

        projects.extend(r.json())
        page += 1

    return projects


def count_commits(project_id):
    r = requests.get(
        f"{BASE_URL}/projects/{project_id}/repository/commits?per_page=1",
        headers={"PRIVATE-TOKEN": GITLAB_TOKEN},
    )

    if "X-Total" in r.headers:
        return int(r.headers["X-Total"])
    return 0


def get_languages(project_id):
    r = requests.get(
        f"{BASE_URL}/projects/{project_id}/languages",
        headers={"PRIVATE-TOKEN": GITLAB_TOKEN},
    )
    return r.json()


def build_svg(projects, total_commits, most_common_lang):
    svg = f'''
<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font-size: 22px; font-weight: bold; fill: #f8f8f2; }}
    .text {{ font-size: 16px; fill: #f8f8f2; }}
    .card {{ fill: #282a36; stroke: #bd93f9; stroke-width: 2; rx: 15; }}
  </style>

  <rect class="card" width="600" height="200" />

  <text x="300" y="40" text-anchor="middle" class="title">
    🚀 GitLab Stats (MARAST01)
  </text>

  <text x="40" y="90" class="text">📦 Projects: {len(projects)}</text>
  <text x="40" y="120" class="text">📝 Commits: {total_commits}</text>
  <text x="40" y="150" class="text">💻 Top language: {most_common_lang}</text>
</svg>
'''
    return svg


def main():
    user_id = get_user()
    projects = get_projects(user_id)

    total_commits = 0
    languages = Counter()

    for p in projects:
        total_commits += count_commits(p["id"])
        langs = get_languages(p["id"])

        for lang, size in langs.items():
            languages[lang] += size

    top_lang = languages.most_common(1)[0][0] if languages else "N/A"

    svg_content = build_svg(projects, total_commits, top_lang)

    with open("gitlab-stats.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)


if __name__ == "__main__":
    main()

