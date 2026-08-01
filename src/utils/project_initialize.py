import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s - %(asctime)s",
)

logger = logging.getLogger(__name__)


def create_project_structure(
    root_path: Path,
    directories: list[str],
) -> None:
    """
    Crée les dossiers du projet dans le répertoire racine.

    Parameters
    ----------
    root_path : Path
        Chemin du dossier racine du projet.
    directories : list[str]
        Liste des sous-dossiers à créer.
    """
    root_path.mkdir(parents=True, exist_ok=True)

    for directory in directories:
        directory_path = root_path / directory
        directory_path.mkdir(parents=True, exist_ok=True)

        logger.info(
            "Dossier créé ou déjà existant : %s",
            directory_path,
        )


def create_project_files(
    root_path: Path,
    files: list[str],
) -> None:
    """
    Crée les fichiers vides du projet sans écraser leur contenu.

    Parameters
    ----------
    root_path : Path
        Chemin du dossier racine du projet.
    files : list[str]
        Liste des fichiers à créer.
    """
    for filename in files:
        file_path = root_path / filename

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not file_path.exists():
            file_path.touch()

            logger.info(
                "Fichier créé : %s",
                file_path,
            )
        else:
            logger.info(
                "Fichier déjà existant : %s",
                file_path,
            )


def main() -> None:
    root_path = Path(
        r"C:\Full_stack\Portfolio\France_energie_intelligence\energy-france-analysis"
    )

    directories = [
        "data/raw",
        "data/processed",
        "data/external",
        "notebooks",
        "src/ingestion",
        "src/preprocessing",
        "src/visualization",
        "src/reporting",
        "src/modeling",
        "src/utils",
        "dashboard",
        "tests",
        "reports",
        "config",
        "models",
        ".github/workflows",
    ]

    files = [
        "README.md",
        "requirements.txt",
        "setup.py",
        "dvc.yaml",
        "params.yaml",
        ".gitignore",
        "app.py",
        "Makefile",
        ".github/workflows/.gitkeep",
    ]

    create_project_structure(root_path, directories)
    create_project_files(root_path, files)


if __name__ == "__main__":
    main()



