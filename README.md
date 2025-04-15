# 🛒 Online Retail ETL Project

Bienvenue dans ce projet **ETL (Extract, Transform, Load)** réalisé en Python, structuré selon les principes de la **programmation orientée objet (POO)**.  
L’objectif est de transformer des données brutes de transactions d’un e-commerce international en un **DataFrame propre, enrichi et prêt à l’analyse**.

---

## 📦 Contexte du Projet

Ce projet s’appuie sur un jeu de données transactionnelles provenant d’un magasin en ligne basé au Royaume-Uni, actif entre **décembre 2010 et décembre 2011**.  
Le jeu de données inclut des informations détaillées sur les **ventes, produits, clients et fournisseurs**.

---

## 🔧 Objectifs

- Nettoyer les données : doublons, valeurs manquantes, annulations
- Traiter les transactions et enrichir les données
- Structurer un pipeline ETL modulaire
- Sauvegarder les données sous format **Parquet**
- Écrire des **tests unitaires** pour chaque composant
- Générer des **logs clairs** pour chaque étape du processus

---

## 🧱 Architecture du Projet

OnlineRetailETL/
│
├── data_cleaner.py              # Nettoyage des données
├── transaction_processor.py     # Traitements analytiques
├── etl_pipeline.py              # Pipeline complet d’orchestration
│
├── tests/
│   ├── test_data_cleaner.py     # Tests unitaires du nettoyage
│   └── test_transaction_processor.py
│
├── data/
│   └── online_retail.csv        # Données sources
│
├── logs/
│   └── etl.log                  # Logs générés
│
└── README.md


---

## 🧠 Ce que vous allez apprendre

✅ Structurer un projet Python de type Data Engineering  
✅ Nettoyer des données réelles avec **pandas**  
✅ Manipuler les **logs** pour suivre les étapes de transformation  
✅ Créer des **classes POO robustes**  
✅ Écrire des **tests unitaires** professionnels avec `pytest`  
✅ Exporter un jeu de données optimisé en **Parquet**

---

## 🚀 Comment exécuter le projet

1. Clonez le repo :
```bash
git clone https://github.com/votre-utilisateur/OnlineRetailETL.git
cd OnlineRetailETL
```

2. Exécutez le pipeline :
````bash
python etl_pipeline.py
````
3. Lancez les tests :

```bash
pytest tests/

```

## 📊 Résultats générés

- DataFrame nettoyé avec calcul du **montant total des transactions**
- Regroupement par **pays**, **mois**, **fournisseur**, et **tranche horaire**
- Export en `.parquet` pour usage futur dans un projet de **DataViz** ou **Machine Learning**

---

## 🧪 Technologies utilisées

- Python 3.10+
- Pandas
- Pytest
- Logging
- Format Parquet

---

## ✨ Auteur

Développé avec ❤️ par **Belkacem Zelmat**  
📧 Contact : belkacem.zelmat@example.com  
🌐 GitHub : [https://github.com/votre-utilisateur/OnlineRetailETL](https://github.com/votre-utilisateur/OnlineRetailETL)


