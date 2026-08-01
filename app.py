import logging
from pathlib import Path

from src.ingestion.downloader import download_file
from config.paths import ZIP_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(name)s - %(message)s - %(asctime)s",
)
# C:\Full_stack\Porfolio\France_energie_intelligence\energy-france-analysis\data\raw\zip

def main() -> None:
    url = "https://eco2mix.rte-france.com/download/eco2mix/eCO2mix_RTE_Annuel-Definitif_2024.zip"

    destination_path = Path("C:/Full_stack/Porfolio/France_energie_intelligence/energy-france-analysis/data/raw/zip/eCO2mix_RTE_Annuel-Definitif_2024.zip")

    downloaded_file = download_file(
        url=url,
        destination_path=destination_path,
    )

    print(f"Fichier disponible : {downloaded_file}")


if __name__ == "__main__":
    main()