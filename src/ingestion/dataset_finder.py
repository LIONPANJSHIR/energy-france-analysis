import logging
import re
import unicodedata
from pathlib import Path

from .territories import METROPOLES, REGIONS


logger = logging.getLogger(__name__)


VALID_DATASET_TYPES = {
    "daily",
    "realtime",
    "consolidated",
    "annual_final",
}


def normalize_text(value: str) -> str:
    """
    Normalise un texte pour faciliter les comparaisons.

    Les accents, espaces, underscores, apostrophes et tirets
    sont normalisés.

    Parameters
    ----------
    value : str
        Texte à normaliser.

    Returns
    -------
    str
        Texte normalisé.
    """
    normalized = unicodedata.normalize("NFKD", value)

    without_accents = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )

    return re.sub(
        pattern=r"[^a-z0-9]+",
        repl="-",
        string=without_accents.lower(),
    ).strip("-")


NORMALIZED_REGIONS = {
    normalize_text(region): region
    for region in REGIONS
}

NORMALIZED_METROPOLES = {
    normalize_text(metropole): metropole
    for metropole in METROPOLES
}


class DatasetFinder:
    """Recherche une archive RTE dans le dossier des données brutes."""

    def __init__(self, raw_directory: Path) -> None:
        """
        Initialise le moteur de recherche.

        Parameters
        ----------
        raw_directory : Path
            Dossier contenant les archives ZIP RTE.
        """
        self.raw_directory = Path(raw_directory)

        if not self.raw_directory.exists():
            raise FileNotFoundError(
                f"Le dossier brut n'existe pas : {self.raw_directory}"
            )

        if not self.raw_directory.is_dir():
            raise NotADirectoryError(
                f"Le chemin n'est pas un dossier : {self.raw_directory}"
            )

    def find(
        self,
        dataset_type: str,
        year: int | None = None,
        location: str | None = None,
        observation_date: str | None = None,
    ) -> Path:
        """
        Recherche l'archive ZIP correspondant aux critères.

        Parameters
        ----------
        dataset_type : str
            Type de données recherché :
            `daily`, `realtime`, `consolidated`
            ou `annual_final`.
        year : int | None
            Année du fichier annuel définitif.
        location : str | None
            Région ou métropole. Si None, le périmètre est national.
        observation_date : str | None
            Date au format YYYY-MM-DD pour un fichier journalier.

        Returns
        -------
        Path
            Chemin du ZIP sélectionné.

        Raises
        ------
        ValueError
            Si les paramètres sont invalides.
        FileNotFoundError
            Si aucun fichier ne correspond.
        RuntimeError
            Si plusieurs fichiers correspondent.
        """
        normalized_dataset_type = normalize_text(dataset_type)

        scope = self.detect_scope(location)

        self._validate_query(
            dataset_type=normalized_dataset_type,
            year=year,
            location=location,
            observation_date=observation_date,
        )

        zip_files = list(self.raw_directory.rglob("*.zip"))

        if not zip_files:
            raise FileNotFoundError(
                "Aucune archive ZIP trouvée dans "
                f"{self.raw_directory.resolve()}."
            )

        matches = [
            zip_path
            for zip_path in zip_files
            if self._matches(
                zip_path=zip_path,
                scope=scope,
                dataset_type=normalized_dataset_type,
                year=year,
                location=location,
                observation_date=observation_date,
            )
        ]

        if not matches:
            available_files = "\n".join(
                f"- {path.name}"
                for path in sorted(zip_files)
            )

            raise FileNotFoundError(
                "Aucune archive ne correspond aux critères.\n"
                f"Périmètre détecté : {scope}\n"
                f"Fichiers disponibles :\n{available_files}"
            )

        if len(matches) > 1:
            matched_files = "\n".join(
                f"- {path.name}"
                for path in sorted(matches)
            )

            raise RuntimeError(
                "Plusieurs archives correspondent aux critères :\n"
                f"{matched_files}"
            )

        selected_file = matches[0]

        logger.info(
            "Archive sélectionnée : %s",
            selected_file,
        )

        return selected_file

    @staticmethod
    def detect_scope(location: str | None) -> str:
        """
        Détermine le périmètre géographique.

        Returns
        -------
        str
            `national`, `regional` ou `metropolitan`.
        """
        if location is None:
            return "national"

        normalized_location = normalize_text(location)

        if normalized_location in NORMALIZED_REGIONS:
            return "regional"

        if normalized_location in NORMALIZED_METROPOLES:
            return "metropolitan"

        raise ValueError(
            f"Territoire inconnu : {location}. "
            "Ajoutez-le dans REGIONS ou METROPOLES "
            "s'il est réellement proposé par RTE."
        )

    @staticmethod
    def _validate_query(
        dataset_type: str,
        year: int | None,
        location: str | None,
        observation_date: str | None,
    ) -> None:
        """Vérifie la cohérence des paramètres."""

        if dataset_type not in {
            "daily",
            "realtime",
            "consolidated",
            "annual-final",
        }:
            raise ValueError(
                f"Type de données invalide : {dataset_type}. "
                "Valeurs acceptées : daily, realtime, "
                "consolidated, annual_final."
            )

        if dataset_type == "annual-final" and year is None:
            raise ValueError(
                "Le paramètre `year` est obligatoire "
                "pour les données annuelles définitives."
            )

        if dataset_type == "daily" and observation_date is None:
            raise ValueError(
                "Le paramètre `observation_date` est obligatoire "
                "pour les données journalières."
            )

        if year is not None and not 2000 <= year <= 2100:
            raise ValueError(
                f"Année invalide : {year}."
            )

        if location is not None and not location.strip():
            raise ValueError(
                "La localisation ne peut pas être vide."
            )

    def _matches(
        self,
        zip_path: Path,
        scope: str,
        dataset_type: str,
        year: int | None,
        location: str | None,
        observation_date: str | None,
    ) -> bool:
        """Vérifie si un ZIP correspond à la demande."""

        normalized_name = normalize_text(zip_path.stem)

        return all(
            (
                self._matches_scope(
                    normalized_name=normalized_name,
                    scope=scope,
                    location=location,
                ),
                self._matches_dataset_type(
                    normalized_name=normalized_name,
                    dataset_type=dataset_type,
                ),
                self._matches_period(
                    normalized_name=normalized_name,
                    dataset_type=dataset_type,
                    year=year,
                    observation_date=observation_date,
                ),
            )
        )

    @staticmethod
    def _matches_scope(
        normalized_name: str,
        scope: str,
        location: str | None,
    ) -> bool:
        """Vérifie le périmètre du fichier."""

        if scope == "national":
            regional_locations = set(NORMALIZED_REGIONS)
            metropolitan_locations = set(NORMALIZED_METROPOLES)

            known_locations = (
                regional_locations | metropolitan_locations
            )

            return not any(
                f"rte-{known_location}-" in normalized_name
                for known_location in known_locations
            )

        if location is None:
            return False

        normalized_location = normalize_text(location)

        expected_prefix = (
            f"eco2mix-rte-{normalized_location}-"
        )

        return normalized_name.startswith(expected_prefix)

    @staticmethod
    def _matches_dataset_type(
        normalized_name: str,
        dataset_type: str,
    ) -> bool:
        """Vérifie le type de données."""

        if dataset_type == "annual-final":
            return "annuel-definitif" in normalized_name

        if dataset_type == "realtime":
            return "en-cours-tr" in normalized_name

        if dataset_type == "consolidated":
            return "en-cours-consolide" in normalized_name

        if dataset_type == "daily":
            forbidden_patterns = (
                "annuel-definitif",
                "en-cours-tr",
                "en-cours-consolide",
            )

            return not any(
                pattern in normalized_name
                for pattern in forbidden_patterns
            )

        return False

    @staticmethod
    def _matches_period(
        normalized_name: str,
        dataset_type: str,
        year: int | None,
        observation_date: str | None,
    ) -> bool:
        """Vérifie l'année ou la date demandée."""

        if dataset_type == "annual-final":
            return (
                year is not None
                and str(year) in normalized_name
            )

        if dataset_type == "daily":
            return (
                observation_date is not None
                and observation_date in normalized_name
            )

        return True