# Data Inventory

## Présentation du jeu de données

Ce jeu de données décrit l'évolution de la consommation électrique, de la production par filière, des échanges internationaux et de plusieurs indicateurs énergétiques en France.

Nom du jeu de données  : eCO2mix_RTE_tempo_2023-2024.xls
Chemin local :data/raw/eCO2mix_RTE_tempo_2023-2024.xls
format : Excel
Nombres d'observations :  35137 
Nombres de variables : 40
frequence apparente : une observation toutes les 15 minutes (à confirmer à l'aide de la documentation officielle)
Les 1er anomalies detecter :
| Anomalie           | Observation                    | À investiguer                |
| ------------------ | ------------------------------ | ---------------------------- |
| Eolien offshore    | Toutes les valeurs sont nulles | Oui                          |
| Dernière ligne     | Contient un texte juridique    | Oui                          |
| Hydraulique        | Valeurs négatives              | Comprendre la convention RTE |
| Bioénergies        | Valeurs négatives              | Comprendre la convention RTE |
| Valeurs manquantes | Plusieurs colonnes incomplètes | Identifier la cause   

## Sources officielle 

Producteur : RTE 
periode couverte : De 2023 à 2024
jeu de données : https://eco2mix.rte-france.com/download/eco2mix/eCO2mix_RTE_Annuel-Definitif_2024.zip       |

## Questions ouverte

- Pourquoi certaines observations n'ont-elles pas de production ?
- Pourquoi certaines colonnes sont-elles entièrement vides ?
- Les valeurs négatives sont-elles normales ?
- Quelle est la convention utilisée par RTE ?
- La fréquence est-elle réellement de 15 minutes ?
- Existe-t-il des doublons temporels ?

## Décision

Le jeu de données est retenu comme source principale du projet.

Avant toute transformation, il sera nécessaire :

- de vérifier la documentation officielle de RTE ;
- de comprendre les conventions utilisées ;
- d'analyser les valeurs manquantes ;
- d'identifier les lignes non liées aux mesures.

## Métadonnées 

Date d'audit : 01/08/2026 - 3:45 AM
Version : 1.0
Auteur : Ly Amadou

## Sources officielle 
