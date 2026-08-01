# import logging
# from pathlib import Path

# import requests


# logger = logging.getLogger(__name__)


# def download_file(
#     url: str,
#     destination_path: Path,
#     overwrite: bool = False,
#     timeout: int = 60,
# ) -> Path:
#     """
#     Télécharge un fichier depuis une URL et l'enregistre localement.

#     Parameters
#     ----------
#     url : str
#         URL du fichier distant.
#     destination_path : Path
#         Chemin complet du fichier à créer.
#     overwrite : bool, default=False
#         Autorise l'écrasement d'un fichier existant.
#     timeout : int, default=60
#         Durée maximale de la requête en secondes.

#     Returns
#     -------
#     Path
#         Chemin du fichier téléchargé.

#     Raises
#     ------
#     ValueError
#         Si l'URL est vide.
#     FileNotFoundError
#         Si la ressource distante retourne une erreur 404.
#     ConnectionError
#         En cas d'erreur réseau.
#     RuntimeError
#         Si le téléchargement échoue ou produit un fichier vide.
#     """
#     if not url.strip():
#         raise ValueError("L'URL de téléchargement ne peut pas être vide.")

#     destination_path = Path(destination_path)
#     destination_path.parent.mkdir(parents=True, exist_ok=True)

#     if destination_path.exists() and not overwrite:
#         logger.info(
#             "Fichier déjà présent, téléchargement ignoré : %s",
#             destination_path,
#         )
#         return destination_path

#     logger.info("Téléchargement du fichier : %s", url)

#     try:
#         with requests.get(
#             url,
#             stream=True,
#             timeout=timeout,
#         ) as response:
#             if response.status_code == 404:
#                 raise FileNotFoundError(
#                     f"Fichier distant introuvable : {url}"
#                 )

#             response.raise_for_status()

#             with destination_path.open("wb") as file:
#                 for chunk in response.iter_content(chunk_size=1024 * 1024):
#                     if chunk:
#                         file.write(chunk)

#     except requests.RequestException as error:
#         if destination_path.exists():
#             destination_path.unlink()

#         raise ConnectionError(
#             f"Échec du téléchargement depuis : {url}"
#         ) from error

#     if not destination_path.exists() or destination_path.stat().st_size == 0:
#         raise RuntimeError(
#             f"Le fichier téléchargé est vide : {destination_path}"
#         )

#     logger.info(
#         "Téléchargement terminé : %s (%s octets)",
#         destination_path,
#         destination_path.stat().st_size,
#     )

#     return destination_path

