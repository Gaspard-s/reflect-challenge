# src/db_manager.py

import pandas as pd
from sqlalchemy import inspect
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
            'id', 'name', 'url', 'displayName', 'modifiedOn', 'lastName', 'firstName', 'login', 'mail', 'birthDate', 'department','manager',
            'rolePrincipal', 'habilitedRoles','legalEntity', 'theoreticalRemuneration', 'employeeNumber'
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
            'id', 'name','code', 'hierarchy', 'parentId', 'isActive','position','level','sortOrder','headID',
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

def insert_new_records(df: pd.DataFrame, engine, table: str, id_column: str = 'id') -> int:
    """
    Insère de nouveaux enregistrements dans une table SQL en évitant les doublons basés sur une colonne d'identifiant.
    
    Args:
        df (pd.DataFrame): DataFrame contenant les enregistrements à insérer.
        engine (sqlalchemy.Engine): L'engine SQLAlchemy connecté à la base de données.
        table (str): Nom de la table dans laquelle insérer les enregistrements.
        id_column (str): Nom de la colonne utilisée pour identifier les doublons.
        
    Returns:
        int: Nombre d'enregistrements insérés.
    """
    if df.empty:
        logging.info(f"Aucun enregistrement à insérer dans la table '{table}'.")
        return 0

    try:
        # Récupérer les identifiants existants dans la table
        existing_ids = pd.read_sql(f"SELECT {id_column} FROM {table}", engine)[id_column].tolist()
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des IDs existants dans la table '{table}': {e}")
        return 0

    # Filtrer les nouveaux enregistrements
    new_df = df[~df[id_column].isin(existing_ids)]

    if new_df.empty:
        logging.info(f"Aucun nouvel enregistrement à insérer dans la table '{table}'.")
        return 0

    try:
        # Insérer les nouveaux enregistrements
        new_df.to_sql(table, engine, if_exists='append', index=False)
        inserted_count = len(new_df)
        return inserted_count
        print("inserted_count")
    except Exception as e:
        logging.error(f"Erreur lors de l'insertion des enregistrements dans la table '{table}': {e}")
        return 0