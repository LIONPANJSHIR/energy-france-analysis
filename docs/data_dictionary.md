# Data Dictionary
## Projet : Analyse du système électrique français

---

## Informations générales

| Élément | Valeur |
|----------|--------|
| **Projet** | France Energy Intelligence |
| **Document** | Data Dictionary |
| **Version** | 1.0 |
| **Statut** | En cours de rédaction |
| **Auteur** | Ly Amadou |
| **Date de création** | 01/08/2026 |
| **Dernière mise à jour** | 01/08/2026 |
| **Source principale** | RTE – eCO2mix |
| **Jeu de données** | eCO2mix_RTE_tempo_2023-2024.xls |

---

# Objectif

Ce document constitue le dictionnaire de données du projet **France Energy Intelligence**.

Il décrit l'ensemble des variables utilisées dans le pipeline de traitement des données. Pour chaque variable sont précisés :

- son rôle métier ;
- son type de données ;
- son traitement dans le pipeline ;
- sa décision de conservation ou de suppression.

Ce document sert de référence unique pour :

- le pipeline ETL ;
- les étapes de prétraitement ;
- les analyses exploratoires ;
- le dashboard interactif ;
- la documentation technique.

---

# Convention utilisée

## Types

- object
- float64
- int64
- datetime64[ns]
- category

---

## Décisions

| Symbole | Signification |
|----------|---------------|
| ✅ | Conserver |
| 🔄 | Transformer |
| ❌ | Supprimer |
| 🟡 | À investiguer |

---

# Variables

## Métadonnées

| Nom original | Nom technique | Description métier | Type actuel | Type final | Pipeline | Décision |
|--------------|---------------|--------------------|-------------|------------|----------|----------|
| Périmètre | perimetre | Périmètre géographique auquel la mesure est associée. | object | category | Vérifier qu'une seule valeur est présente puis supprimer. | ❌ |
| Nature | nature | Nature des données publiées (définitives, consolidées...). | object | category | Vérifier qu'une seule valeur est présente puis supprimer. | ❌ |
| Date | date | Date de l'observation. | object | datetime64[ns] | Conversion en datetime. | 🔄 |
| Heures | heure | Heure de l'observation. | object | string | Fusion avec Date pour créer un timestamp. | 🔄 |

---

## Consommation

| Nom original | Nom technique | Description métier | Type actuel | Type final | Pipeline | Décision |
|--------------|---------------|--------------------|-------------|------------|----------|----------|
| Consommation | consommation_mw | Puissance électrique consommée sur le réseau français (MW). | float64 | float64 | Vérifier le type numérique et les valeurs manquantes prévues. | ✅ |
| Prévision J-1 | prevision_j1_mw | Prévision de la consommation électrique réalisée la veille (J-1). | float64 | float64 | Vérifier le type numérique et les valeurs manquantes. | ✅ |
| Prévision J | prevision_j_mw | Prévision de la consommation électrique réalisée pour le jour J. | float64 | float64 | Vérifier le type numérique et les valeurs manquantes. | ✅ |

---

## Production

| Nom original | Nom technique | Description métier | Type actuel | Type final | Pipeline | Décision |
|--------------|---------------|--------------------|-------------|------------|----------|----------|
| Fioul | fioul_mw | Production électrique issue des centrales au fioul. | float64 | float64 | Vérifier le type numérique. | ✅ |
| Charbon | charbon_mw | Production électrique issue des centrales à charbon. | float64 | float64 | Vérifier le type numérique. | ✅ |
| Gaz | gaz_mw | Production électrique issue des centrales à gaz. | float64 | float64 | Vérifier le type numérique. | ✅ |
| Nucléaire | nucleaire_mw | Production électrique d'origine nucléaire. | float64 | float64 | Vérifier le type numérique. | ✅ |
| Eolien | eolien_mw | Production électrique d'origine éolienne. | float64 | float64 | Vérifier le type numérique. | ✅ |
| Solaire | solaire_mw | Production électrique d'origine solaire. | float64 | float64 | Vérifier le type numérique. | ✅ |
| Hydraulique | hydraulique_mw | Production électrique d'origine hydraulique. | float64 | float64 | Vérifier les conventions métier. | ✅ |
| Pompage | pompage_mw | Puissance consommée pour le pompage des STEP. | float64 | float64 | Vérifier les valeurs négatives attendues. | ✅ |
| Bioénergies | bioenergies_mw | Production électrique issue des bioénergies. | float64 | float64 | Vérifier les conventions métier. | ✅ |

---

## Échanges internationaux

| Nom original | Nom technique | Description métier | Type actuel | Type final | Pipeline | Décision |
|--------------|---------------|--------------------|-------------|------------|----------|----------|
| Ech. physiques | echanges_physiques_mw | Solde des échanges physiques d'électricité avec les pays voisins. | float64 | float64 | Vérifier les valeurs positives et négatives. | ✅ |
| Angleterre | angleterre_mw | Échanges avec le Royaume-Uni. | float64 | float64 | Vérifier les valeurs positives et négatives. | ✅ |
| Espagne | espagne_mw | Échanges avec l'Espagne. | float64 | float64 | Vérifier les valeurs positives et négatives. | ✅ |
| Italie | italie_mw | Échanges avec l'Italie. | float64 | float64 | Vérifier les valeurs positives et négatives. | ✅ |
| Suisse | suisse_mw | Échanges avec la Suisse. | float64 | float64 | Vérifier les valeurs positives et négatives. | ✅ |
| Allemagne-Belgique | allemagne_belgique_mw | Échanges avec l'Allemagne et la Belgique. | float64 | float64 | Vérifier les valeurs positives et négatives. | ✅ |

---

## Sous-catégories de production

*(Insérer ici les colonnes Gaz TAC, Gaz CCG, Hydraulique STEP, Biomasse, etc.)*

---

## Stockage

*(Stockage batterie, Déstockage batterie)*

---

## Éolien détaillé

*(Éolien terrestre, Éolien offshore)*

---

# Historique des modifications

| Version | Date | Auteur | Description |
|----------|------|--------|-------------|
| 1.0 | 01/08/2026 | Ly Amadou | Première version du dictionnaire des données. |