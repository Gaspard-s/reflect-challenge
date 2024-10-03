# tests/test_data_processor.py

import pytest
import pandas as pd
from src.data_processor import process_users, process_departments, process_contracts_from_users, transform_user_data
import json

def test_process_users_empty():
    users = []
    df = process_users(users)
    assert df.empty

def test_process_users_non_empty():
    users = [
        {"id": 1, "name": "John Doe", "department": {"name": "Engineering"}, "rolePrincipal": {"name": "Developer"}, "legalEntity": {"name": "Company A"}, "applicationData": {"theoreticalRemuneration": {"value": 50000}}}
    ]
    df = process_users(users)
    assert not df.empty
    assert df.loc[0, 'name'] == "John Doe"


def test_transform_user_data():
    # Données d'entrée couvrant tous les attributs récupérés depuis l'API
    data = {
        "id": [1],
        "name": ["John Doe"],
        "url": ["https://example.com/api/v3/users/1"],
        "displayName": ["Doe John"],
        "modifiedOn": ["2023-10-01T12:00:00Z"],
        "lastName": ["Doe"],
        "firstName": ["John"],
        "login": ["jdoe"],
        "mail": ["jdoe@example.com"],
        "birthDate": ["1990-01-01T00:00:00Z"],
        "department": [{"name": "Engineering"}],
        "manager": [{"id": 2, "name": "Jane Smith"}],
        "rolePrincipal": [{"name": "Senior Developer"}],
        "legalEntity": [{"name": "Company A"}],
        "employeeNumber": ["E12345"],
        "applicationData": [{"theoreticalRemuneration": {"value": 75000}}],
        "habilitedRoles": [
            [
                {"id": 101, "name": "Role A", "url": "https://example.com/api/v3/roles/101"},
                {"id": 102, "name": "Role B", "url": "https://example.com/api/v3/roles/102"}
            ]
        ]
    }
    
    # Création du DataFrame d'entrée
    df_input = pd.DataFrame(data)
    
    # Application de la transformation
    transformed_df = transform_user_data(df_input)
    
    # Assertions pour vérifier chaque transformation
    assert transformed_df.loc[0, 'id'] == 1
    assert transformed_df.loc[0, 'name'] == "John Doe"
    assert transformed_df.loc[0, 'url'] == "https://example.com/api/v3/users/1"
    assert transformed_df.loc[0, 'displayName'] == "Doe John"
    assert transformed_df.loc[0, 'modifiedOn'] == "2023-10-01T12:00:00Z"
    assert transformed_df.loc[0, 'lastName'] == "Doe"
    assert transformed_df.loc[0, 'firstName'] == "John"
    assert transformed_df.loc[0, 'login'] == "jdoe"
    assert transformed_df.loc[0, 'mail'] == "jdoe@example.com"
    assert transformed_df.loc[0, 'birthDate'] == "1990-01-01T00:00:00Z"
    assert transformed_df.loc[0, 'department'] == "Engineering"
    assert transformed_df.loc[0, 'rolePrincipal'] == "Senior Developer"
    assert transformed_df.loc[0, 'legalEntity'] == "Company A"
    assert transformed_df.loc[0, 'employeeNumber'] == "E12345"
    assert transformed_df.loc[0, 'theoreticalRemuneration'] == 75000
    assert 'applicationData' not in transformed_df.columns
    
    # Vérification de la colonne 'habilitedRoles'
    expected_habilited_roles = json.dumps(['Role A', 'Role B'])
    assert transformed_df.loc[0, 'habilitedRoles'] == expected_habilited_roles
    
    # Vérification des colonnes supprimées
    columns_present = transformed_df.columns.tolist()
    columns_to_not_include = ['dtContractStart', 'dtContractEnd']
    for column in columns_to_not_include:
        assert column not in columns_present, f"Colonne {column} ne devrait pas être présente dans le DataFrame transformé."


def test_process_departments_empty():
    departments = []
    df = process_departments(departments)
    assert df.empty

def test_process_departments_non_empty():
    departments = [
        {"id": 1, "name": "Engineering", "hierarchy": "/engineering/", "parentId": None, "headID": 10, "users": [], "currentUsers": [], "currentUsersCount": 0}
    ]
    df = process_departments(departments)
    assert not df.empty
    assert df.loc[0, 'name'] == "Engineering"

def test_process_contracts_from_users_empty():
    users = []
    df = process_contracts_from_users(users)
    assert df.empty

def test_process_contracts_from_users_non_empty():
    users = [
        {
            "id": 1,
            "dtContractStart": "2023-01-01",
            "dtContractEnd": "2023-12-31",
            "applicationData": {"theoreticalRemuneration": {"value": 50000}}
        }
    ]
    df = process_contracts_from_users(users)
    assert not df.empty
    assert df.loc[0, 'user_id'] == 1
    assert df.loc[0, 'start_date'] == "2023-01-01"
    assert df.loc[0, 'end_date'] == "2023-12-31"
    assert df.loc[0, 'theoretical_remuneration'] == 50000
