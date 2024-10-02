# src/main.py

from api_client import LuccaAPIClient
from data_processor import (
    process_users,
    process_departments,
    process_contracts_from_users,
    transform_user_data,
    clean_user_data
)
from db_manager import initialize_db, insert_new_records
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

def main():
    # Définir le chemin absolu pour la base de données
    db_path = os.path.abspath('reflect_db.sqlite')
    DATABASE_URI = os.getenv('DATABASE_URI', f'sqlite:///{db_path}')
    engine = create_engine(DATABASE_URI)

    # Initialiser la base de données uniquement si le fichier n'existe pas
    if not os.path.exists(db_path):
        logging.info("Initialisation de la base de données...")
        initialize_db(engine)
    else:
        logging.info("La base de données existe déjà. Aucune initialisation nécessaire.")

    # Créer une instance du client API
    try:
        client = LuccaAPIClient()
    except ValueError as ve:
        logging.error(ve)
        sys.exit(1)

    # Récupérer les utilisateurs depuis l'API
    logging.info("Récupération des utilisateurs...")
    users = client.get_users(params={
        'fields': 'id,name,url,displayName,modifiedOn,lastName,firstName,login,mail,birthDate,department,rolePrincipal,legalEntity,employeeNumber,dtContractStart,dtContractEnd,applicationData'})

    if not users:
        logging.error("Aucun utilisateur récupéré. Vérifiez le token API et les permissions.")
        sys.exit(1)

    # Traiter les données des utilisateurs
    users_df = process_users(users)
    users_df = transform_user_data(users_df)

    # Extraire les contrats et insérer dans la base de données
    logging.info("Extraction des contrats depuis les utilisateurs...")
    contracts_df = process_contracts_from_users(users)
    if not contracts_df.empty:
        logging.info("Insertion des nouveaux contrats dans la base de données...")
        inserted_contracts = insert_new_records(contracts_df, engine, 'contracts', id_column='user_id')
        logging.info(f"{inserted_contracts} nouveaux contrats insérés dans la base de données.")
    else:
        logging.warning("Aucun contrat extrait des utilisateurs.")

    # Nettoyer les données des utilisateurs en supprimant les colonnes liées aux contrats
    users_df_cleaned = clean_user_data(users_df)

    # Insérer uniquement les nouveaux utilisateurs
    logging.info("Insertion des nouveaux utilisateurs dans la base de données...")
    #to_csv = users_df_cleaned.to_csv('data/users.csv', index=False)
    inserted_users = insert_new_records(users_df_cleaned, engine, 'users', id_column='id')
    logging.info(f"{inserted_users} nouveaux utilisateurs insérés dans la base de données.")

    # Récupérer les départements depuis l'API
    logging.info("Récupération des départements...")
    departments = client.get_departments(params={
        'fields': 'id,name,hierarchy,parentId,headID,users,currentUsers,currentUsersCount',
    })

    if not departments:
        logging.warning("Aucun département récupéré.")

    # Traiter les données des départements
    departments_df = process_departments(departments)

    # Insérer uniquement les nouveaux départements
    logging.info("Insertion des nouveaux départements dans la base de données...")
    inserted_departments = insert_new_records(departments_df, engine, 'departments', id_column='id')
    logging.info(f"{inserted_departments} nouveaux départements insérés dans la base de données.")

    logging.info("Terminé.")


if __name__ == '__main__':
    # Créer le dossier 'data' s'il n'existe pas
    if not os.path.exists('data'):
        os.makedirs('data')
    main()
