import pandas as pd
import json
from typing import List, Dict, Any

def process_users(users: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Processus de transformation des données des utilisateurs.

    Args:
        users (List[Dict[str, Any]]): Liste des utilisateurs.

    Returns:
        pd.DataFrame: DataFrame contenant les données des utilisateurs.
    """
    if not users:
        return pd.DataFrame()
    users_df = pd.DataFrame(users)
    return users_df

def extract_role_ids(role_field: Any) -> List[int]:
    """
    Extracts a list of role IDs from a JSON-formatted string or a list of role dicts.

    Args:
        role_field (str or list): JSON-formatted string or list of role dictionaries.

    Returns:
        List[int]: List of role IDs.
    """
    try:
        if isinstance(role_field, str):
            roles = json.loads(role_field)
        elif isinstance(role_field, list):
            roles = role_field
        elif role_field is None:
            return []
  
        return [role['name'] for role in roles if isinstance(role, dict) and 'name' in role]
    except (json.JSONDecodeError, TypeError) as e:
        return []

def transform_user_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms user data by extracting department names, legal entities, principal roles,
    theoretical remunerations, and habilited role IDs.

    Args:
        df (pd.DataFrame): DataFrame containing user data.

    Returns:
        pd.DataFrame: Transformed DataFrame.
    """
    # Extract department name
    df['department'] = df['department'].apply(
        lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown'
    )
    
    # Extract legal entity name
    df['legalEntity'] = df['legalEntity'].apply(
        lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown'
    )
    
    # Extract principal role name
    df['rolePrincipal'] = df['rolePrincipal'].apply(
        lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown'
    )

    # Extract principal role name
    df['manager'] = df['manager'].apply(
        lambda x: x.get('name', 'Unknown') if isinstance(x, dict) else 'Unknown'
    )
    
    # Extract theoretical remuneration
    df['theoreticalRemuneration'] = df['applicationData'].apply(
        lambda x: x.get('theoreticalRemuneration', {}).get('value', 'Unknown') 
        if isinstance(x, dict) else 'Unknown'
    )
    
    # Extract habilited role IDs and serialize as JSON strings
    df['habilitedRoles'] = df['habilitedRoles'].apply(extract_role_ids)
    df['habilitedRoles'] = df['habilitedRoles'].apply(json.dumps)
    
    # Drop unnecessary columns
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


def extract_user_ids(user_field: Any) -> List[str]:
    """
    Extracts a list of user IDs from a JSON-formatted string or a list of user dicts.

    Args:
        user_field (str or list): JSON-formatted string or list of user dictionaries.

    Returns:
        List[int]: List of user IDs.
    """
    try:
        if isinstance(user_field, str):
            users = json.loads(user_field)
        elif isinstance(user_field, list):
            users = user_field
        elif user_field is None:
            return []
        return [user['name'] for user in users if isinstance(user, dict) and 'name' in user]
    except (json.JSONDecodeError, TypeError) as e:
        return []

def process_departments(departments: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Converts a list of department dictionaries into a pandas DataFrame and extracts user IDs.

    Args:
        departments (List[Dict[str, Any]]): List of department data.

    Returns:
        pd.DataFrame: Processed DataFrame with user IDs extracted and serialized.
    """
    if not departments:
        return pd.DataFrame()
    
    departments_df = pd.DataFrame(departments)
    
    # Extract user IDs from 'users' and 'currentUsers' columns
    for col in ['users', 'currentUsers']:
        if col in departments_df.columns:
            departments_df[col] = departments_df[col].apply(extract_user_ids)
            departments_df[col] = departments_df[col].apply(json.dumps)  # Serialize to JSON string
    
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
