"""Class DataCleanner responsable du nettoyage des données"""

import pandas as pd 
import logging

#configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
file_handler = logging.FileHandler('logs/datacleaner.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class DataCleaner: 

    #Creation du constructeur 
    def __init__(self, df : pd.DataFrame):
        self.df = df
    
    #méthode de suppression toutes les lignes avec des doublons
    def remove_duplicates(self):
        #supprimer les lignes avec des doublons
        init_len = len(self.df) # pour les logs
        self.df.drop_duplicates(inplace=True)
        logging.info(f"{init_len - len (self.df)} doublons supprimés.") #affichage du log de la fonction remove_duplicates qui affiche le nombre de doublons supprimés

    
    #méthode de traitement des valeurs manquantes
    def handle_missing_values(self):
        missing_before = self.df.isnull().sum() # compter les valeurs manquantes avant le traitement pour comparer dans les logs
        self.df.dropna(subset=['CustomerID', 'InvoiceNo', 'StockCode'], inplace=True) # Supprimer les lignes ou StockCode, CustomerID, InvoiceNo  sont NaN
        self.df['Description'].fillna('Aucune description n\'est disponible', inplace=True)  # Remplacer les NaN par Aucune description
        self.df['Quantity'].fillna(self.df['Quantity'].median(), inplace=True)  # Remplir avec la médiane
        self.df['UnitPrice'].fillna(self.df['UnitPrice'].mean(), inplace=True)  # Remplir avec la moyenne
        self.df['Country'].fillna(self.df['Country'].mode()[0], inplace=True)  # Remplir avec le pays le  plus fréquente

        logging.info(f"Valeurs manquantes traitée. Le nombre des valeurs était de : \n{missing_before}")

    #méthode pour garder que les transactions non annulées 
    def filter_valid_transactions(self):
        init_count = len(self.df) # compter le nombre de ligne avant suppression pour comparer dans les logs
        self.df = self.df[~self.df['InvoiceNo'].astype(str).str.startswith('C')]         #suppression de toutes transaction qui commence par 'C'
        logging.info(f"{init_count - len(self.df)} transaction annulées supprimées! ")

        return self.df


# Exécution des méthodes de la classe afin de visualiser les logs
if __name__ == "__main__":
    #importer le dataset
    df_test_logs = pd.read_excel("Online Retail.xlsx")

    dataCleaner = DataCleaner(df_test_logs)
    dataCleaner.remove_duplicates()
    dataCleaner.handle_missing_values()
    dataCleaner.filter_valid_transactions()

    print("Les logs sont enregistrés dans le fichier logs/datacleaner.log")