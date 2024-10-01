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
    data = {
        "id": 1,
        "name": "John Doe",
        "department": {"name": "Engineering"},
        "rolePrincipal": {"name": "Developer"},
        "legalEntity": {"name": "Company A"},
        "applicationData": {"theoreticalRemuneration": {"value": 50000}}
    }
    df = pd.DataFrame([data])
    transformed_df = transform_user_data(df)
    
    assert transformed_df.loc[0, 'department'] == "Engineering"
    assert transformed_df.loc[0, 'rolePrincipal'] == "Developer"
    assert transformed_df.loc[0, 'legalEntity'] == "Company A"
    assert transformed_df.loc[0, 'theoreticalRemuneration'] == 50000
    assert 'applicationData' not in transformed_df.columns

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
