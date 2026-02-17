import requests
import os
import sys

# --- CONFIGURACIÓN ---
GITLAB_USER = "MARAST01" 
TOKEN = os.environ.get("GITLAB_TOKEN")

if not TOKEN:
    print("ERROR: No se encontró la variable de entorno GITLAB_TOKEN")
    sys.exit(1)

headers = {"PRIVATE-TOKEN": TOKEN}

# --- 1. OBTENER DATOS DE GITLAB ---
# Datos del usuario
try:
    response_user = requests.get(f"https://gitlab.com/api/v4/users?username={GITLAB_USER}", headers=headers)
    response_user.raise_for_status() # Lanza error si no es 200 OK
    
    data = response_user.json()
    if not data:
        print(f"ERROR: Usuario {GITLAB_USER} no encontrado.")
        sys.exit(1)
        
    user_data = data[0] # La búsqueda devuelve una lista
    user_id = user_data.get('id')
    name = user_data.get('name')
    username = user_data.get('username')
    avatar_url = user_data.get('avatar_url')

    # Datos de eventos (para simular actividad/commits recientes)
    # Esto cuenta las acciones de los últimos 90 días aprox
    response_events = requests.get(f"https://gitlab.com/api/v4/users/{user_id}/events", headers=headers)
    events = response_events.json()
    total_events = len(events) if isinstance(events, list) else 0

except Exception as e:
    print(f"ERROR conectando a GitLab: {e}")
    sys.exit(1)

# --- 2. DISEÑO SVG (Estilo similar a tus GitHub Stats) ---
# Colores: Fondo #151515 (oscuro), Texto Titulo #ff79c6 (rosa), Texto Normal #fff
svg_content = f"""
<svg width="495" height="195" viewBox="0 0 495 195" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #ff79c6; }}
    .stat {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: #fff; }}
    .label {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #9f9f9f; }}
  </style>
  
  <rect x="0.5" y="0.5" width="494" height="194" rx="4.5" fill="#141321" stroke="#e4e2e2" stroke-opacity="0.5"/>
  
  <text x="25" y="35" class="header">GitLab Stats</text>
  
  <text x="25" y="80" class="stat">User:</text>
  <text x="100" y="80" class="label">{username}</text>
  
  <text x="25" y="110" class="stat">ID:</text>
  <text x="100" y="110" class="label">{user_id}</text>
  
  <text x="25" y="140" class="stat">Recent Activity:</text>
  <text x="140" y="140" class="label">{total_events} events (last 20 items)</text>

  <path d="M460 160 L440 160 L450 130 Z" fill="#fc6d26"/>
  <circle cx="400" cy="100" r="40" stroke="#ff79c6" stroke-width="4" fill="none" opacity="0.8" />
  <text x="400" y="105" text-anchor="middle" class="header" font-size="20">GL</text>
</svg>
"""

# --- 3. GUARDAR ---
with open("gitlab-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"SVG generado exitosamente para {username}")
