import argparse
import hashlib
import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"

API_URL = (
    "https://api.github.com/repos/"
    "sportsdataverse/sportsdataverse-data/"
    "releases/tags/nba_stats_shots"
)

HEADERS = {
    "User-Agent": "NBA-Shot-Evolution",
    "Accept": "application/vnd.github+json",
}


def get_release():
    request = Request(API_URL, headers=HEADERS)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_asset(asset):
    name = asset["name"]
    target = RAW / name
    expected_size = asset["size"]
    temporary = RAW / (name + ".part")

    if target.exists() and target.stat().st_size == expected_size:
        logging.info("Archivo existente: %s", name)
        status = "already_exists"
    else:
        logging.info("Descargando: %s", name)
        request = Request(
            asset["browser_download_url"],
            headers={"User-Agent": "NBA-Shot-Evolution"},
        )
        try:
            with urlopen(request, timeout=120) as response:
                with temporary.open("wb") as output:
                    shutil.copyfileobj(response, output)

            if temporary.stat().st_size != expected_size:
                raise ValueError("Tamano descargado incorrecto")

            temporary.replace(target)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise

        status = "downloaded"
        logging.info("Descarga completa: %s", name)

    return {
        "filename": name,
        "status": status,
        "source_url": asset["browser_download_url"],
        "size_bytes": target.stat().st_size,
        "sha256": sha256_file(target),
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--years",
        nargs="+",
        type=int,
        default=[2024],
    )
    args = parser.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(REPORTS / "ingestion.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    try:
        release = get_release()
        assets = {
            asset["name"]: asset
            for asset in release["assets"]
        }

        records = []
        for year in args.years:
            filename = f"shots_{year}.parquet"
            if filename not in assets:
                raise ValueError(f"No existe: {filename}")

            records.append(download_asset(assets[filename]))

        manifest = RAW / "ingestion_manifest.json"
        manifest.write_text(
            json.dumps(records, indent=2),
            encoding="utf-8",
        )

        print("\nPIPELINE DE ADQUISICION COMPLETADO")
        for record in records:
            print(record["filename"], record["status"])

    except Exception:
        logging.exception("Error en el pipeline")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
