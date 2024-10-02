# src/data_processor.py

import pandas as pd
import json
from typing import List, Dict, Any

def process_users(users: List[Dict[str, Any]]) -> pd.DataFrame:
    if not users:
        return pd.DataFrame()
    users_df = pd.DataFrame(users)
    return users_df

def transform_user_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforme les données des utilisateurs en extrayant les noms des départements,
    entités légales, rôles principaux et rémunérations théoriques.

    Args:
        df (pd.DataFrame): DataFrame contenant les données des utilisateurs.

    Returns:
        pd.DataFrame: DataFrame transformé.
    """
    # Extraire le nom du département
    df['department'] = df['department'].apply(
        lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown'
    )
    
    # Extraire le nom de l'entité légale
    df['legalEntity'] = df['legalEntity'].apply(
        lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown'
    )
    
    # Extraire le nom du rôle principal
    df['rolePrincipal'] = df['rolePrincipal'].apply(
        lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown'
    )
    
    # Extraire la rémunération théorique
    df['theoreticalRemuneration'] = df['applicationData'].apply(
        lambda x: x.get('theoreticalRemuneration', {}).get('value', 'Unknown') 
        if isinstance(x, dict) else 'Unknown'
    )
    
    df.drop(columns=['applicationData'], errors='ignore', inplace=True)
    return df

def process_contracts_from_users(users: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Processus de transformation des données des contrats à partir des données des utilisateurs.

    Args:
        users (List[Dict[str, Any]]): Liste des utilisateurs.

    Returns:
        pd.DataFrame: DataFrame contenant les données des contrats.
    """
    contracts = []
    for user in users:
        contract = {
            "user_id": user.get("id"),
            "start_date": user.get("dtContractStart"),
            "end_date": user.get("dtContractEnd"),
            "theoretical_remuneration": user.get("applicationData", {}).get("theoreticalRemuneration", {}).get("value", "Unknown")
        }
        contracts.append(contract)
    contracts_df = pd.DataFrame(contracts)
    return contracts_df

def process_departments(departments: List[Dict[str, Any]]) -> pd.DataFrame:
    if not departments:
        return pd.DataFrame()
    
    departments_df = pd.DataFrame(departments)
    
    # Sérialiser les colonnes contenant des listes
    list_columns = ['users', 'currentUsers']
    for col in list_columns:
        if col in departments_df.columns:
            departments_df[col] = departments_df[col].apply(lambda x: json.dumps(x) if isinstance(x, list) else json.dumps([]))
    
    return departments_df

def clean_user_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Supprime les colonnes liées aux contrats des données des utilisateurs.

    Args:
        df (pd.DataFrame): DataFrame contenant les données des utilisateurs.

    Returns:
        pd.DataFrame: DataFrame nettoyé sans les colonnes liées aux contrats.
    """
    columns_to_drop = ['dtContractStart', 'dtContractEnd', 'theoreticalRemuneration']
    df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')
    return df_cleaned
