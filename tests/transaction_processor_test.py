# transaction_processor_test est un fichier  python qui contient un Test Unitaire des méthodes de la classe TransactionProcessor 

import pandas as pd
import pytest
from transaction_processor import  TransactionProcessor # import des méthodes de la classe transaction_processor
from pytest import approx


@pytest.fixture

# Creation d'un dataset pour le test
def sample_data():
    """Fixture pour créer un DataFrame de test"""
    data = {
        'InvoiceNo': ['536365', '536366', 'C536367', '536368', '536369'],
        'StockCode': ['85123A', '71053', '84406B', '84406B', '84879'],
        'Description': ['WHITE HANGING HEART T-LIGHT HOLDER', 
                        'WHITE METAL LANTERN', 
                        'CREAM CUPID HEARTS COAT HANGER',
                        'CREAM CUPID HEARTS COAT HANGER',
                        'ASSORTED COLOUR BIRD ORNAMENT'],
        'Quantity': [6, 6, -2, 8, 6],
        'InvoiceDate': pd.to_datetime(['2010-12-01 08:26', '2010-12-01 08:28', 
                                       '2010-12-01 08:34', '2010-12-01 08:34',
                                       '2010-12-01 08:35']),
        'UnitPrice': [2.55, 3.39, 2.75, 2.75, 1.69],
        'CustomerID': ['17850', '17850', '17850', '17850', '17850'],
        'Country': ['United Kingdom', 'United Kingdom', 'France', 'France', 'Germany'],
      #  'Supplier': ['F001', 'F002', 'F003', 'F003', 'F004']
    }
    df = pd.DataFrame(data)
    return df

@pytest.fixture
def processor(sample_data):
    #créer une instance de TransactionProcessor
    return TransactionProcessor(sample_data)

#Test du calcul du montant total des transactions 
def test_calculate_total_amount(processor):
    
    processor.calculate_total_amount()
    expected_totals = [15.30, 20.34, -5.50, 22.00, 10.14]
    assert 'TotalAmount' in processor.df.columns
    assert processor.df['TotalAmount'].tolist() == approx(expected_totals, rel=1e-2)

#Test du regroupement des transactions par pays
def test_group_by_country(processor):
    processor.calculate_total_amount()
    result = processor.group_by_country()
    expected_countries = ['France', 'Germany', 'United Kingdom']
    assert result['Country'].tolist() == expected_countries

#Test de l'agrégation des données mensuelles
def test_aggregate_monthly_data(processor):
    
    processor.calculate_total_amount()
    result = processor.aggregate_monthly_data()
    assert len(result) == 1  # Tous les enregistrements sont du même mois
    assert result.iloc[0]['total_sales'] == sum(processor.df['Quantity'] * processor.df['UnitPrice'])

#Test des statistiques sur le produit le plus rentable en France
def test_calcul_stat_data(processor):
    
    processor.calculate_total_amount()
    processor.calcul_stat_data()
    france_data = processor.df[processor.df['Country'] == 'France']
    top_product = france_data.groupby('Description')['Quantity'].sum().idxmax()
    assert top_product == 'CREAM CUPID HEARTS COAT HANGER'

#Test de l'agrégation des données des fournisseurs
def test_aggregate_supplier_data(processor):
    
    processor.calculate_total_amount()
    result = processor.aggregate_supplier_data()
    assert len(result) == 4  # 4 fournisseurs uniques
    assert result.iloc[0]['Supplier'] == 'F003'  # Le fournisseur F003 devrait être en tête

#Test de l'agrégation des données mondiales avec un mapping pays-continent
def test_aggregate_world_data(processor):
    
    mapping_data = {
        'Country': ['United Kingdom', 'France', 'Germany'],
        'Continent': ['Europe', 'Europe', 'Europe']
    }
    mapping_df = pd.DataFrame(mapping_data)
    processor.calculate_total_amount()
    result = processor.aggregate_world_data()
