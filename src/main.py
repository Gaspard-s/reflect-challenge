# main.py

from api_client import LuccaAPIClient
from data_processor import process_users, process_departments, process_contracts_from_users, transform_user_data
import os
import sys
import logging
import pandas as pd
from sqlalchemy import create_engine
import json

# Configurer le logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("data/app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def save_to_db(df: pd.DataFrame, table_name: str, engine):
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Données sauvegardées dans la table '{table_name}'.")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde dans la table '{table_name}': {e}")

def main():
    # Définir le chemin absolu pour la base de données
    db_path = os.path.abspath('reflect_db.sqlite')
    DATABASE_URI = os.getenv('DATABASE_URI', f'sqlite:///{db_path}')
    engine = create_engine(DATABASE_URI)

    # Créer une instance du client API
    client = LuccaAPIClient()

    logging.info("Récupération des utilisateurs...")
    users = client.get_users(params={
        'fields': 'id,name,login,mail,birthDate,department,rolePrincipal,legalEntity,dtContractStart,dtContractEnd,applicationData',
    })

    if not users:
        logging.error("Aucun utilisateur récupéré. Vérifiez le token API et les permissions.")
        sys.exit(1)

    users_df = process_users(users)

    users_df = transform_user_data(users_df)
    # Sauvegarder les utilisateurs dans la base de données
    logging.info("Sauvegarde des utilisateurs dans la base de données...")
    save_to_db(users_df, 'users', engine)
    logging.info(f"{len(users_df)} utilisateurs sauvegardés dans la base de données.")

    # Extraire et sauvegarder les contrats
    logging.info("Extraction des contrats depuis les utilisateurs...")
    contracts_df = process_contracts_from_users(users)
    if not contracts_df.empty:
        logging.info("Sauvegarde des contrats dans la base de données...")
        save_to_db(contracts_df, 'contracts', engine)
        logging.info(f"{len(contracts_df)} contrats sauvegardés dans la base de données.")
    else:
        logging.warning("Aucun contrat extrait des utilisateurs.")

    # Récupérer les départements
    logging.info("Récupération des départements...")
    departments = client.get_departments(params={
        'fields': 'id,name,hierarchy,parentId,headID,users,currentUsers,currentUsersCount',
    })

    if not departments:
        logging.warning("Aucun département récupéré.")

    departments_df = process_departments(departments)

    # Sauvegarder les départements dans la base de données
    logging.info("Sauvegarde des départements dans la base de données...")
    save_to_db(departments_df, 'departments', engine)
    logging.info(f"{len(departments_df)} départements sauvegardés dans la base de données.")

if __name__ == '__main__':
    # Créer le dossier 'data' s'il n'existe pas
    if not os.path.exists('data'):
        os.makedirs('data')
    main()
