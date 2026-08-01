import logging
from pathlib import Path
from zipfile import BadZipFile, ZipFile, is_zipfile


logger = logging.getLogger(__name__)


SUPPORTED_EXTENSIONS = {
    ".xls",
    ".xlsx",
    ".csv",
    ".txt",
}


def extract_data_file(
    zip_path: Path,
    destination_directory: Path,
    overwrite: bool = False,
) -> Path:
    """
    Extrait le fichier de données contenu dans une archive RTE.

    Parameters
    ----------
    zip_path : Path
        Chemin de l'archive ZIP.
    destination_directory : Path
        Répertoire d'extraction.
    overwrite : bool, default=False
        Autorise le remplacement d'un fichier déjà extrait.

    Returns
    -------
    Path
        Chemin du fichier extrait.
    """
    zip_path = Path(zip_path)
    destination_directory = Path(destination_directory)

    if not zip_path.exists():
        raise FileNotFoundError(
            f"Archive introuvable : {zip_path}"
        )

    if not zip_path.is_file():
        raise ValueError(
            f"Le chemin n'est pas un fichier : {zip_path}"
        )

    if not is_zipfile(zip_path):
        raise ValueError(
            f"Archive ZIP invalide : {zip_path}"
        )

    destination_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        with ZipFile(zip_path, mode="r") as archive:
            data_members = [
                member
                for member in archive.namelist()
                if (
                    not member.endswith("/")
                    and Path(member).suffix.lower()
                    in SUPPORTED_EXTENSIONS
                )
            ]

            if not data_members:
                raise ValueError(
                    "Aucun fichier XLS, XLSX, CSV ou TXT "
                    f"trouvé dans {zip_path.name}."
                )

            if len(data_members) > 1:
                raise RuntimeError(
                    "Plusieurs fichiers de données trouvés "
                    f"dans l'archive : {data_members}"
                )

            member_name = data_members[0]

            destination_path = (
                destination_directory
                / Path(member_name).name
            )

            if destination_path.exists() and not overwrite:
                logger.info(
                    "Fichier déjà extrait : %s",
                    destination_path,
                )
                return destination_path

            if destination_path.exists():
                destination_path.unlink()

            logger.info(
                "Extraction de %s",
                member_name,
            )

            with archive.open(member_name) as source:
                with destination_path.open("wb") as destination:
                    while chunk := source.read(1024 * 1024):
                        destination.write(chunk)

    except BadZipFile as error:
        raise RuntimeError(
            f"Archive ZIP corrompue : {zip_path}"
        ) from error

    if not destination_path.exists():
        raise RuntimeError(
            "Le fichier extrait est introuvable."
        )

    if destination_path.stat().st_size == 0:
        destination_path.unlink(missing_ok=True)

        raise RuntimeError(
            "Le fichier extrait est vide."
        )

    logger.info(
        "Extraction terminée : %s",
        destination_path,
    )

    return destination_path