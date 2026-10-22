import os
from pathlib import Path
from databricks import sql

# Cargar credenciales privadas desde el archivo .env
env_path = Path.home() / ".databricks.env"

if not env_path.exists():
    raise FileNotFoundError("No se encontró el archivo .databricks.env")

for line in env_path.read_text(encoding="utf-8-sig").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")

with sql.connect(
    server_hostname=os.environ["DATABRICKS_SERVER_HOSTNAME"],
    http_path=os.environ["DATABRICKS_HTTP_PATH"],
    access_token=os.environ["DATABRICKS_TOKEN"]
) as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM workspace.nba_shot_iq.silver_shots"
        )
        total = cursor.fetchone()[0]

print("CONEXIÓN EXITOSA")
print("TIROS EN SILVER:", total)