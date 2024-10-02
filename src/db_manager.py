# src/db_manager.py

import pandas as pd
from sqlalchemy import create_engine, inspect
import logging

def initialize_db(engine):
    """
    Initialise la base de données en créant les tables si elles n'existent pas.
    
    Args:
        engine (sqlalchemy.Engine): L'engine SQLAlchemy connecté à la base de données.
    """
    inspector = inspect(engine)

    # Créer la table 'users' si elle n'existe pas
    if not inspector.has_table("users"):
        pd.DataFrame(columns=[
            'id', 'name', 'url', 'displayName', 'modifiedOn', 'lastName', 'firstName', 'login', 'mail', 'birthDate', 'department',
            'rolePrincipal', 'legalEntity', 'theoreticalRemuneration', 'employeeNumber'
        ]).to_sql('users', engine, if_exists='replace', index=False)
        logging.info("Création de la table 'users'.")

    # Créer la table 'contracts' si elle n'existe pas
    if not inspector.has_table("contracts"):
        pd.DataFrame(columns=[
            'user_id', 'start_date', 'end_date', 'theoretical_remuneration'
        ]).to_sql('contracts', engine, if_exists='replace', index=False)
        logging.info("Création de la table 'contracts'.")

    # Créer la table 'departments' si elle n'existe pas
    if not inspector.has_table("departments"):
        pd.DataFrame(columns=[
            'id', 'name', 'hierarchy', 'parentId', 'headID',
            'users', 'currentUsers', 'currentUsersCount'
        ]).to_sql('departments', engine, if_exists='replace', index=False)
        logging.info("Création de la table 'departments'.")

def get_existing_ids(engine, table, id_column='id'):
    """
    Récupère les IDs existants d'une table donnée.
    
    Args:
        engine (sqlalchemy.Engine): L'engine SQLAlchemy connecté à la base de données.
        table (str): Le nom de la table.
        id_column (str, optional): Le nom de la colonne ID. Par défaut 'id'.
    
    Returns:
        set: Un ensemble contenant les IDs existants.
    """
    query = f"SELECT {id_column} FROM {table}"
    df = pd.read_sql(query, engine)
    return set(df[id_column].tolist())

def insert_new_records(df, engine, table, id_column='id'):
    """
    Insère de nouveaux enregistrements dans une table en évitant les doublons basés sur l'ID.
    
    Args:
        df (pd.DataFrame): Le DataFrame contenant les nouvelles données à insérer.
        engine (sqlalchemy.Engine): L'engine SQLAlchemy connecté à la base de données.
        table (str): Le nom de la table.
        id_column (str, optional): Le nom de la colonne ID. Par défaut 'id'.
    
    Returns:
        int: Le nombre de nouveaux enregistrements insérés.
    """
    existing_ids = get_existing_ids(engine, table, id_column)
    new_df = df[~df[id_column].isin(existing_ids)]

    if not new_df.empty:
        new_df.to_sql(table, engine, if_exists='append', index=False)
        logging.info(f"Inséré {len(new_df)} nouveaux enregistrements dans la table '{table}'.")
        return len(new_df)
    else:
        logging.info(f"Aucun nouvel enregistrement à insérer dans la table '{table}'.")
        return 0
