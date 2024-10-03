# api_client.py

import requests
from typing import Dict, Any, List, Optional
import logging
from dotenv import load_dotenv
import os

class LuccaAPIClient:
    def __init__(self):
        self.base_url = 'https://reflect2-sandbox.ilucca-demo.net'
        self.api_token = 'caf8058b-b7ec-4df2-85e3-a673b5466e97'

        if not self.api_token:
            raise ValueError("Le token API est manquant.")

        self.headers = {
            'Authorization': f'lucca application={self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Configuration du logger
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"API_TOKEN chargé: {self.api_token}")
        self.logger.info(f"BASE_URL chargé: {self.base_url}")

    def get_users(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Récupère la liste des utilisateurs depuis l'API Lucca.

        Args:
            params (dict): Paramètres de requête supplémentaires.

        Returns:
            List[Dict[str, Any]]: Liste des utilisateurs.
        """
        endpoint = f'{self.base_url}/api/v3/users?formerEmployees=true'
        params = params
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)

            if response.status_code == 200:
                data = response.json()

                # Vérifier si la réponse contient un message d'erreur
                if 'message' in data:
                    self.logger.error(f"Erreur dans la réponse : {data['message']}")
                    if data['message'].lower() == "rate limit exceeded":
                        self.logger.error("Limite de taux atteinte.")
                    return []


                users = data.get('data', {}).get('items', [])
                return users

            elif response.status_code == 429:
                self.logger.error("Limite de taux atteinte (HTTP 429).")
                return []

            else:
                response.raise_for_status()

        except Exception as err:
            self.logger.error(f'Erreur lors de la récupération des utilisateurs : {err}')
            return []

    def get_departments(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Récupère la liste des départements depuis l'API Lucca.

        Args:
            params (dict): Paramètres de requête supplémentaires.

        Returns:
            List[Dict[str, Any]]: Liste des départements.
        """
        endpoint = f'{self.base_url}/api/v3/departments'
        params = params or {}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)

            if response.status_code == 200:
                data = response.json()

                # Vérifier si la réponse contient un message d'erreur
                if 'message' in data:
                    self.logger.error(f"Erreur dans la réponse : {data['message']}")
                    if data['message'].lower() == "rate limit exceeded":
                        self.logger.error("Limite de taux atteinte.")
                    return []

                departments = data.get('data', {}).get('items', [])

                return departments

            elif response.status_code == 429:
                self.logger.error("Limite de taux atteinte (HTTP 429).")
                return []

            else:
                response.raise_for_status()

        except Exception as err:
            self.logger.error(f'Erreur lors de la récupération des départements : {err}')
            return []
