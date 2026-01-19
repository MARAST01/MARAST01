import requests
import os

# Configuración
GITLAB_USER = "MARAST01" # Tu usuario de GitLab
TOKEN = os.environ.get("GITLAB_TOKEN")

# 1. Obtener datos de GitLab
headers = {"PRIVATE-TOKEN": TOKEN}
response = requests.get(f"https://gitlab.com/api/v4/users/{GITLAB_USER}", headers=headers)
user_data = response.json()

# Si usas GitLab self-hosted o necesitas contar commits, la lógica se expande aquí.
# Por ahora, usaremos datos básicos del perfil para el ejemplo.

# 2. Crear el contenido SVG (Diseño simple)
svg_content = f"""
<svg width="300" height="100" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#1e1e1e" rx="10" />
  <text x="20" y="35" fill="white" font-family="Arial" font-size="18">GitLab Stats</text>
  <text x="20" y="70" fill="#fc6d26" font-family="Arial" font-size="14">User: {user_data.get('username', 'Unknown')}</text>
  <text x="150" y="70" fill="#999" font-family="Arial" font-size="12">ID: {user_data.get('id', 'N/A')}</text>
</svg>
"""

# 3. Guardar el archivo
with open("gitlab-stats.svg", "w") as f:
    f.write(svg_content)

print("SVG Generado correctamente.")
