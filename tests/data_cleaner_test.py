# data_cleaner_test est un fichier  python qui contient un Test Unitaire des méthodes de la classe DataCleanner 

import pandas as pd
import pytest
from data_cleaner import  DataCleaner # import des méthodes de la classe DataCleaner

@pytest.fixture

# Creation d'un dataset pour le test
def sample_df(): 
      data = {
        "InvoiceNo": ["123456", "123456", "C123457", "123458", None],
        "StockCode": ["A1234", "A1234", "B5678", "C91011", "D1213"],
        "Description": ["Item1", "Item1", None, "Item3", "Item4"],
        "Quantity": [1, 1, 2, None, 3],
        "InvoiceDate": ["2021-01-01", "2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04"],
        "UnitPrice": [10.0, 10.0, 15.0, 20.0, 5.0],
        "CustomerID": [12345, 12345, 67890, None, 13579],
        "Country": ["France", "France", "UK", "Germany", "Spain"]
    }
      
      df = pd.DataFrame(data)
      return df

def test_remove_duplicates(sample_df):
    # Tester si les doublons sont réelement supprimés
    cleaner = DataCleaner(sample_df)
    cleaner.remove_duplicates()
    assert len(cleaner.df) == 4 # tester si réelement on avait qu'un seul doublon 

def test_handle_missing_values(sample_df):
    # Tester le bon traitment des valeurs manquantes
    cleaner = DataCleaner(sample_df)
    cleaner.handle_missing_values()
    assert cleaner.df.isnull().sum().sum() == 0 # pour tester si réalement les 4 Nan on était traité ( le double sum() pour compte le totale des NaN dans le dataframe)

def test_filter_valid_transaction(sample_df):
     #Tester si les transaction annulée sont supprimé
     cleaner = DataCleaner(sample_df)
     df_filtred = cleaner.filter_valid_transactions()
     assert not df_filtred['InvoiceNo'].astype(str).str.startswith('C').any() #si la méthode est correct, aucun num commence par 'C'



     