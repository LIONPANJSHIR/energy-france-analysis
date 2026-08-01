import logging
from pathlib import Path

import pandas as pd

from .dataset_finder import DatasetFinder
from .extractor import extract_data_file
from .reader import read_data_file


logger = logging.getLogger(__name__)


class IngestionPipeline:
    """Orchestre l'ingestion des données brutes RTE."""

    def __init__(
        self,
        raw_directory: Path,
        extraction_directory: Path | None = None,
    ) -> None:
        self.raw_directory = Path(raw_directory)

        self.extraction_directory = (
            Path(extraction_directory)
            if extraction_directory is not None
            else self.raw_directory / "extracted"
        )

        self.finder = DatasetFinder(
            raw_directory=self.raw_directory,
        )

    def run(
        self,
        dataset_type: str,
        year: int | None = None,
        location: str | None = None,
        observation_date: str | None = None,
        overwrite_extraction: bool = False,
    ) -> pd.DataFrame:
        """
        Exécute le pipeline complet d'ingestion.
        """
        logger.info("Démarrage du pipeline d'ingestion.")

        zip_path = self.finder.find(
            dataset_type=dataset_type,
            year=year,
            location=location,
            observation_date=observation_date,
        )

        extracted_path = extract_data_file(
            zip_path=zip_path,
            destination_directory=self.extraction_directory,
            overwrite=overwrite_extraction,
        )

        dataframe = read_data_file(
            file_path=extracted_path,
        )

        logger.info("Pipeline d'ingestion terminé.")

        return dataframe

    def run_years(
    self,
    years: list[int],
    location: str | None = None,
    overwrite_extraction: bool = False,
    ) -> pd.DataFrame:
        """
        Charge et concatène plusieurs années de données RTE.

        Parameters
        ----------
        years : list[int]
            Années à charger.
        location : str | None
            Région ou métropole. None pour le national.
        overwrite_extraction : bool
            Autorise la réextraction des fichiers.

        Returns
        -------
        pd.DataFrame
            Données brutes concaténées.
        """
        if not years:
            raise ValueError("La liste des années ne peut pas être vide.")

        dataframes: list[pd.DataFrame] = []

        for year in sorted(set(years)):
            logger.info("Ingestion de l'année %s", year)

            dataframe = self.run(
                dataset_type="annual_final",
                year=year,
                location=location,
                overwrite_extraction=overwrite_extraction,
            )

            dataframe = dataframe.copy()
            dataframe["source_year"] = year

            dataframes.append(dataframe)

        combined_dataframe = pd.concat(
            dataframes,
            ignore_index=True,
        )

        logger.info(
            "Concaténation terminée : %s lignes, %s colonnes",
            combined_dataframe.shape[0],
            combined_dataframe.shape[1],
        )

        return combined_dataframe