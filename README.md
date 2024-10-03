# Reflect Challenge

Author : Gaspard Saliou

# Présentation projet

### 1. `main.py`

**Description** :  
C'est le point d'entrée principal du projet. Il coordonne l'exécution globale en effectuant les actions suivantes :
- Initialisation de la base de données SQLite si elle n'existe pas.
- Récupération des utilisateurs et des départements depuis l'API Lucca.
- Traitement et transformation des données récupérées.
- Insertion des nouveaux enregistrements dans la base de données tout en évitant les doublons.
- Affichage des informations dans la console.

### 2. `api_client.py`

**Description** :  
Ce fichier gère les interactions avec l'API Lucca. Il contient la classe `LuccaAPIClient` qui :
- Configure les en-têtes et l'authentification nécessaires pour les requêtes API.
- Fournit des méthodes pour récupérer les données des utilisateurs et des départements via des requêtes HTTP GET.
- Gère les erreurs liées aux requêtes API.

### 3. `data_processor.py`

**Description** :  
Ce fichier est responsable du traitement et de la transformation des données brutes récupérées depuis l'API. Il inclut les fonctions suivantes :
- **Extraction des IDs** : `extract_user_ids` et `extract_role_ids` pour extraire les identifiants des utilisateurs et des rôles à partir des champs JSON.
- **Transformation des données** : `transform_user_data` pour nettoyer et transformer les données des utilisateurs (par exemple, extraire les noms des départements, entités légales, rôles principaux, etc.).
- **Traitement des contrats** : `process_contracts_from_users` pour extraire les informations contractuelles des utilisateurs.
- **Nettoyage des données** : `clean_user_data` pour supprimer les colonnes inutiles liées aux contrats après l'extraction.

### 4. `db_manager.py`

**Description** :  
Ce fichier gère toutes les opérations liées à la base de données SQLite. Il contient les fonctions suivantes :
- **Initialisation de la base de données** : `initialize_db` pour créer les tables (`users`, `contracts`, `departments`) si elles n'existent pas déjà.
- **Insertion des enregistrements** : `insert_new_records` pour insérer de nouveaux enregistrements dans les tables en évitant les doublons basés sur une colonne identifiant (`id_column`).


# Installation

To set up the project on your local machine, follow these steps:


1. **Create a Virtual Environment**

    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. **Install Dependencies**

    ```
    pip install -r requirements.txt
    ```

4. **Initialize the Database**

    The database will be initialized automatically when you run the main script if it does not already exist.


# Usage

Once the installation and configuration steps are complete, you can run the project to fetch and store data.

**replace the token and url in launch.sh with the correct values**
    
    export API_URL= url
    export LUCCA_API_TOKEN= token

**If the launch file has not the permission to be executed**

    chmod 755 launch.sh

**Run the Main Script**
    
    ./launch.sh
    
This script will:
- Initialize the SQLite database if it doesn't exist.
- Fetch users and departments from the Lucca API.
- Process and transform the fetched data.
- Insert new records into the SQLite database, ensuring no duplicates.
- Log the operations to the console.


# Testing

To ensure the reliability of each function, the project includes unit tests.

**Run the Tests**
    
    pytest
    
This command will discover and run all tests located in the `tests/` directory.

# Database access

**To see if data is incorporate in the db**
  

    sqlite3 reflect_db.sqlite


**To List the tables**

    
    .tables
    

**If you wanna see Users Table**

    
    SELECT * FROM users LIMIT 5;
    