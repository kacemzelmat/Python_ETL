"""Class etl_pipeline qui orchestre le processus ETL en appelant les méthodes des autres classes"""


import pandas as pd 
import logging
from data_cleaner import DataCleaner
from transaction_processor import TransactionProcessor
from continent import   country_continent_mapping

#configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
file_handler = logging.FileHandler('logs/etl_pipeline.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Etl_Pipeline:

    #Création du constructeur
    def __init__(self, df : pd.DataFrame):
        self.df = df

    def run_pipeline(self):
        # cette méthode execute la pipeline ETL compelte en appelant toutes les méthodes des autres classes
        logging.info("Début de la pipeline ETL..")

        """Etape 01: Nettoyage"""
        logging.info("Etape 01: Nettoyage")
        cleaner = DataCleaner(self.df)
        cleaner.remove_duplicates()
        cleaner.handle_missing_values()
        cleaner.filter_valid_transactions()

        """Etape 02: Traitement des Transactions"""
        logging.info("Etape 02: Traitement des Transactions")
        processor = TransactionProcessor(cleaner.df)
        processor.calculate_total_amount()
        country_sales = processor.group_by_country()
        monthly_stat = processor.aggregate_monthly_data()
        processor.calcul_stat_data()
        supplier_aggregation = processor.aggregate_supplier_data()

        """Etape 03: Les données mondiales"""
        logging.info("Etape 03: Les données mondiales")
        #On va refaire un nouvel appel des méthodes, on a besoin des données avec des transaction annulées pour ce traitement
        cleaner_no_cancel = DataCleaner(self.df)
        cleaner_no_cancel.remove_duplicates()
        cleaner_no_cancel.handle_missing_values()
        processor_no_cancel = TransactionProcessor(cleaner_no_cancel.df)
        processor_no_cancel.calculate_total_amount()
        processor_no_cancel.aggregate_world_data()

        logging.info("Pipeline ETL terminé avec succès :)")

        # Stocker le résultat final
        self.df = processor.df

    def save_as_parquet(self, path):
        """
        Sauvegarde le DataFrame final sous format Parquet."""
        logging.info(f"Enregistrement du fichier parquet dans {path}...")
        self.df[self.df.select_dtypes(include=['object']).columns] = self.df.select_dtypes(include=['object']).apply(pd.to_numeric, errors='coerce').astype('Int64')

        self.df.to_parquet(path, index=False)
        logging.info("Fichier parquet enregistré avec succès.")


# Exécution des méthodes de la classe afin de visualiser les logs
if __name__ == "__main__":
    #importer le dataset
    df_test_logs = pd.read_excel("Online Retail.xlsx")

    etl_pipeline = Etl_Pipeline(df_test_logs)
    etl_pipeline.run_pipeline()
    etl_pipeline.save_as_parquet("data/transactions_final.parquet")

    print("Les logs sont enregistrés dans le fichier logs/etl_pipeline.log")