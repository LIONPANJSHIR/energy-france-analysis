from dataclasses import dataclass
from datetime import date
from enum import Enum


class DatasetScope(str, Enum):
    """Périmètres géographiques disponibles."""

    NATIONAL = "national"
    REGION = "region"
    METROPOLE = "metropole"


class DatasetType(str, Enum):
    """Types de jeux de données éCO2mix disponibles."""

    DAILY = "daily"
    REALTIME = "realtime"
    CONSOLIDATED = "consolidated"
    ANNUAL_FINAL = "annual_final"


@dataclass(frozen=True)
class DatasetQuery:
    """
    Décrit le jeu de données RTE recherché.

    Parameters
    ----------
    scope : DatasetScope
        Périmètre géographique recherché.
    dataset_type : DatasetType
        Type de données recherché.
    year : int | None
        Année recherchée pour les données annuelles définitives.
    location : str | None
        Nom de la région ou de la métropole.
    observation_date : date | None
        Date recherchée pour un fichier journalier.
    """

    scope: DatasetScope
    dataset_type: DatasetType
    year: int | None = None
    location: str | None = None
    observation_date: date | None = None

    def validate(self) -> None:
        """Vérifie la cohérence de la requête."""

        if self.scope in {
            DatasetScope.REGION,
            DatasetScope.METROPOLE,
        } and not self.location:
            raise ValueError(
                "Le nom de la région ou de la métropole est obligatoire."
            )

        if (
            self.dataset_type == DatasetType.ANNUAL_FINAL
            and self.year is None
        ):
            raise ValueError(
                "L'année est obligatoire pour un fichier annuel définitif."
            )

        if (
            self.dataset_type == DatasetType.DAILY
            and self.observation_date is None
        ):
            raise ValueError(
                "La date est obligatoire pour un fichier journalier."
            )

        if self.year is not None and not 2000 <= self.year <= 2100:
            raise ValueError(
                f"Année invalide : {self.year}."
            )