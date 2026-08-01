import logging
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


logger = logging.getLogger(__name__)


def download_file(
    url: str,
    destination_path: Path,
    overwrite: bool = False,
) -> Path:
    """
    Télécharge un fichier depuis une URL et l'enregistre localement.

    Parameters
    ----------
    url : str
        URL du fichier source.
    destination_path : Path
        Chemin local du fichier à créer.
    overwrite : bool, default=False
        Autorise ou non l'écrasement d'un fichier existant.

    Returns
    -------
    Path
        Chemin du fichier téléchargé.

    Raises
    ------
    ValueError
        Si l'URL est vide.
    FileExistsError
        Si le fichier existe déjà et que overwrite=False.
    RuntimeError
        Si le téléchargement échoue.
    """
    if not url.strip():
        raise ValueError("L'URL de téléchargement ne peut pas être vide.")

    destination_path = Path(destination_path)

    if destination_path.exists() and not overwrite:
        logger.info(
            "Le fichier existe déjà, téléchargement ignoré : %s",
            destination_path,
        )
        return destination_path

    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info(
        "Téléchargement du fichier depuis : %s",
        url,
    )

    try:
        with urlopen(url, timeout=60) as response:
            content = response.read()

        destination_path.write_bytes(content)

    except (HTTPError, URLError, TimeoutError, OSError) as error:
        logger.exception(
            "Échec du téléchargement depuis : %s",
            url,
        )
        raise RuntimeError(
            f"Impossible de télécharger le fichier depuis {url}"
        ) from error

    if destination_path.stat().st_size == 0:
        destination_path.unlink(missing_ok=True)
        raise RuntimeError(
            "Le fichier téléchargé est vide."
        )

    logger.info(
        "Téléchargement terminé : %s (%s octets)",
        destination_path,
        destination_path.stat().st_size,
    )

    return destination_path