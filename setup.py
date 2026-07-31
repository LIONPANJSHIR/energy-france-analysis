import os
import logging
from pathlib import Path

# project_name = "energie-france-analysis"
ROOT = Path("C:\Full_stack\Porfolio\France_energie_intelligence\energy-france-analysis")

logging.basicConfig(
level= logging.INFO ,
format = "%(levelname)s - %(message)s - %(asctime)s"
)

list_of_files = [
  f"{ROOT}/src/utils/project_initialize.py"
]

for path in list_of_files :
  filepath = Path(path)
  filedir , filename = os.path.split(filepath)
  if filedir != "" :
    os.makedirs(filedir,exist_ok=True)
    logging.info(f"le dossier '{filedir} a etais crée avec succés")

  if (not filepath.exists()) or (os.path.getsize(filepath) == 0):
    with open (filepath , "w") :
      filepath.touch()        
    logging.info(f"Le fichier '{filepath}' a été créé avec succès.")
  else:
    logging.info(f"Le fichier '{filepath}' existe déjà et n’est pas vide.")