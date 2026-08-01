import logging
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


OLE_XLS_SIGNATURE = bytes.fromhex(
    "D0 CF 11 E0 A1 B1 1A E1"
)

ZIP_SIGNATURES = (
    b"PK\x03\x04",
    b"PK\x05\x06",
    b"PK\x07\x08",
)


def detect_file_format(file_path: Path) -> str:
    """
    Détecte le format réel d'un fichier.

    Returns
    -------
    str
        `xls`, `xlsx` ou `text`.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {file_path}"
        )

    with file_path.open("rb") as file:
        signature = file.read(8)

    if signature.startswith(OLE_XLS_SIGNATURE):
        return "xls"

    if signature.startswith(ZIP_SIGNATURES):
        return "xlsx"

    return "text"


def read_data_file(
    file_path: Path,
    sheet_name: int | str = 0,
) -> pd.DataFrame:
    """
    Charge un fichier brut RTE dans un DataFrame.

    Aucune transformation métier n'est appliquée.

    Parameters
    ----------
    file_path : Path
        Chemin du fichier à lire.
    sheet_name : int | str, default=0
        Feuille Excel à lire.

    Returns
    -------
    pd.DataFrame
        Données brutes chargées.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Le chemin n'est pas un fichier : {file_path}"
        )

    if file_path.stat().st_size == 0:
        raise ValueError(
            f"Le fichier est vide : {file_path}"
        )

    file_format = detect_file_format(file_path)

    logger.info(
        "Format détecté pour %s : %s",
        file_path.name,
        file_format
    )

    try:
        if file_format == "xls":
            dataframe = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                engine="xlrd"
            )

        elif file_format == "xlsx":
            dataframe = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                engine="openpyxl"
            )

        else:
            dataframe = read_tabular_text(file_path)

    except Exception as error:
        logger.exception(
            "Échec de la lecture de %s",
            file_path,
        )

        raise RuntimeError(
            f"Impossible de lire le fichier : {file_path}"
        ) from error

    if dataframe.empty:
        raise ValueError(
            f"Aucune observation dans le fichier : {file_path}"
        )

    logger.info(
        "Fichier chargé : %s lignes, %s colonnes",
        dataframe.shape[0],
        dataframe.shape[1],
    )

    return dataframe


def read_tabular_text(file_path: Path) -> pd.DataFrame:
    """
    Lit un fichier texte tabulé en testant plusieurs encodages.
    """
    encodings = (
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin-1",
    )

    last_error: Exception | None = None

    for encoding in encodings:
        try:
            dataframe = pd.read_csv(
                file_path,
                sep="\t",
                encoding=encoding,
                low_memory=False,
                index_col=False,
            )

            logger.info(
                "Encodage utilisé : %s",
                encoding,
            )

            return dataframe

        except UnicodeDecodeError as error:
            last_error = error

    raise UnicodeError(
        f"Encodage non reconnu pour {file_path}"
    ) from last_error