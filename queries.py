import pandas as pd
from db import engine
df =pd.read_csv("financecore_clean (3).csv")

from sqlalchemy import text
import pandas as pd
from db import engine


# KPIs
def get_kpis():
    query = """
    SELECT 
        COUNT(*) AS total_transactions,
        SUM(montant) AS total_ca,
        COUNT(DISTINCT client_id) AS clients_actifs,
        AVG(marge) AS marge_moyenne
    FROM transactions;
    """
    return pd.read_sql(query, engine)

# Time series

def get_time_series():
    query = """
    SELECT *
    FROM (
        SELECT 
            DATE_TRUNC('month', date_transaction) AS mois,
            SUM(CASE WHEN type_operation='debit' THEN montant ELSE 0 END) AS debit,
            SUM(CASE WHEN type_operation='credit' THEN montant ELSE 0 END) AS credit
        FROM transactions
        GROUP BY DATE_TRUNC('month', date_transaction)
    ) t
    ORDER BY mois;
    """

    df = pd.read_sql(query, engine)
    return df


# Données risques
def get_risk_data():
    query = """
    SELECT client_id, score_credit_client, montant, categorie_risque
    FROM transactions;
    """
    return pd.read_sql(query, engine)