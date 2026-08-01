import logging
from pathlib import Path

from src.ingestion import IngestionPipeline


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(levelname)s - %(name)s - "
        "%(message)s - %(asctime)s"
    ),
)


def main() -> None:
    pipeline = IngestionPipeline(
        raw_directory=Path("data/raw"),
    )

    dataframe = pipeline.run_years(
        years= [] #list(range(2014, 2024)),
    )

    print(dataframe.shape)
    print(dataframe["source_year"].value_counts())
    print(dataframe.head())


if __name__ == "__main__":
    main()
