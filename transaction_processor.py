"""Class transaction_processor qui gère la logique métier pour les transactions"""

import pandas as pd 
import logging
from continent import country_continent_mapping

#configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
file_handler = logging.FileHandler('logs/transactionprocessor.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class TransactionProcessor:

    #Création du constructeur
    def __init__(self, df : pd.DataFrame):
        self.df = df

    
    #Méthode pour calculer le montant total de chaque transaction
    def calculate_total_amount(self):

        logging.info("Calcule du montant total de chaque transaction..") #log pour indiquer le debut de la méthode
        self.df['TotalAmount'] = self.df['Quantity'] * self.df['UnitPrice'] # calculer le total ( quantité * prix unitaire) et ajouter le resultat dans une nouvelle colonne
        df_log = self.df
        logging.info(f"Calcule du total terminée et une nouvelle colonne 'TotalAmount' est ajoutée. Voici un appercu : \n {df_log.head()}")


    #méthode pour regrouper les données par pays puis calculer la somme total des montants des transactions pour chaque pays
    def group_by_country(self):

        logging.info("Regroupement des donées par pays et calcul de la somme total des ventes par pays...") #log indiquer le debut du traitement de la methode
        country_sales = self.df.groupby('Country')['TotalAmount'].sum().reset_index() #grouper par pays puis calculer la somme des ventes pour chacun
        logging.info(f"Traitement terminée, voici un appercu des ventes par pays \n : {country_sales.head()}")
        return country_sales
    
    
    #méthode pour  Calculer des statistiques mensuelles
    def aggregate_monthly_data(self):

        logging.info("Calcule des statistiques mensuelles..")#log indiquer le debut du traitement de la methode

        self.df['Month'] = self.df['InvoiceDate'].dt.to_period('M') #extraire le mois de chaque transaction

        #aggregation des données mensuelles
        monthly_data = self.df.groupby('Month').agg(
            total_sales = ('TotalAmount','sum'),
            transaction_count = ('InvoiceNo','count' )
        ).reset_index()

        logging.info(f"Calcule des staistiques mensuelles terminé, voici un appercu : \n{monthly_data.head()}")#affichage des logs
        return monthly_data
    

    #méthode de statistiques sur les données
    def calcul_stat_data(self):

        logging.info("Calcul des statistiques ..")

        #affichage des produit ayant rapporté le plus de gains en France
        france_data = self.df[self.df['Country'] == 'France'] # filtrage sur la France
        top_product = france_data.groupby('Description')['TotalAmount'].sum().idxmax() # les prduits ayant plus de gain en france
        logging.info(f"Le produit ayant rapporté plus de gains en France est: {top_product}")


        #Analyse l'heure à laquelle le nombre de transactions est le plus élevé
        france_data['Hour'] = france_data['InvoiceDate'].dt.hour #conversion en heure
        hour_analysis = france_data.groupby('Hour')['InvoiceNo'].nunique().reset_index() #regrouper par Heure et compter le nombre de transaction
        peak_hour = hour_analysis.loc[hour_analysis['InvoiceNo'].idxmax()] #Chercher l'heure avec le plus grand nombre de yransaction
        logging.info(f"L'\heure avec le plus grand nombre de transaction est: {peak_hour['Hour']}H.") #affichage du log


    #méthode pour avoir des informations sur les fournisseurs 
    def aggregate_supplier_data(self):

        logging.info("Etude sur les des données des fournisseurs")

        #Importation des données des fournisseur
        supplier_df = pd.read_csv('Supplier.csv')

        #Fusionner les 2 dataset
        merged_df = pd.merge(self.df, supplier_df, on="InvoiceNo")

        #Eliminer les transactions annulées
        valid_transactions = merged_df[~merged_df['InvoiceNo'].str.startswith('C')]

        #Agrégation des ventes par fournisseur
        supplier_sales = valid_transactions.groupby('Supplier')['TotalAmount'].sum().reset_index()

        #Classement des fournisseurs
        supplier_sales = supplier_sales.sort_values(by="TotalAmount", ascending=False)

        #affichage du log du classement des fournisseurs 
        logging.info(f"Le classement des TOP fournisseurs est: \n {supplier_sales.head()}")

        #################################################
        #Filtrage des fournisseurs sur l'année 2011 a UK
        data_uk_2011 = valid_transactions[(valid_transactions['InvoiceDate'].dt.year == 2011 ) & (valid_transactions['Country']== "United Kingdom")]
        #Aggregation des ventes par fournisseurs UK 2011
        supplier_sales_uk = data_uk_2011.groupby('Supplier')['TotalAmount'].sum().reset_index()
        #Classement des fournisseurs UK 2011
        supplier_sales_uk = supplier_sales_uk.sort_values(by="TotalAmount", ascending=False)
        #affichage du log du classement des fournisseurs UK 2011
        logging.info(f"Le classement des TOP fournisseurs des UK en 2011 est: \n {supplier_sales_uk.head()}")


    #méthode pour  Ajouter un fichier de mapping au projet permettant d’associer les pays présents dans le fichier à leurs continents
    def aggregate_world_data(self):

        logging.info("Aggregation des données mondiales..") # intialisation du log 

        #Ajouter la colonne Continent en mappant la colonne Country en utlisant les données dans continent.py
        self.df['Continent'] = self.df['Country'].map(lambda x: country_continent_mapping.get(x,"Unknown"))
        world_data = self.df

        #Regrouper les ventes par continent
        continent_sales = world_data.groupby('Continent')['TotalAmount'].sum().reset_index()

        #Triée les ventes par continent
        continent_sales = continent_sales.sort_values(by='TotalAmount',ascending=False)
        logging.info(f"Le classement des ventes par Continent est: \n  {continent_sales}")

        logging.info("Identification du contient avec plus d'opérations annulées...")

        #Calculer les transctions annulées par continent 
         # Suppression des valeurs NaN dans InvoiceNo
        world_data = world_data.dropna(subset=['InvoiceNo'])#suppression des valeurs NaN
        cancelled_transactions = world_data[world_data['InvoiceNo'].astype(str).str.startswith('C')]#filtrer les transactions annulées 
        cancelled_by_continent = cancelled_transactions.groupby('Continent').size().reset_index(name='CancelledTransactions')#aggreger les transactions annullées par continent

        #Continent avec le plus grand nombre de yransactions annulées
        peak_cancelled_continent =    cancelled_by_continent.loc[cancelled_by_continent['CancelledTransactions'].idxmax()]
        logging.info(f"Le continent avec le plus grand nombre de transactions annulées est: {peak_cancelled_continent['Continent']}")



# Exécution des méthodes de la classe afin de visualiser les logs
if __name__ == "__main__":
    #importer le dataset

    
    df_test_logs = pd.read_excel("Online Retail.xlsx")

    transaction_processor = TransactionProcessor(df_test_logs)
    transaction_processor.calculate_total_amount()
    transaction_processor.group_by_country()
    transaction_processor.aggregate_monthly_data()
    transaction_processor.calcul_stat_data()
    transaction_processor.aggregate_supplier_data()
    transaction_processor.aggregate_world_data()

    print("Les logs sont enregistrés dans le fichier logs/transactionprocessor.log")


        