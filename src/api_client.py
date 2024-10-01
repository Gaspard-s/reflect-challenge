# api_client.py

import requests
from typing import Dict, Any, List, Optional
import logging
from dotenv import load_dotenv
import os

class LuccaAPIClient:
    def __init__(self):
        load_dotenv()  # Charger les variables d'environnement depuis le fichier .env
        self.base_url = os.getenv('API_URL', 'https://reflect2-sandbox.ilucca-demo.net')
        self.api_token = os.getenv('LUCCA_API_TOKEN')  # Utiliser la variable d'environnement

        if not self.api_token:
            raise ValueError("Le token API est manquant.")

        self.headers = {
            'Authorization': f'lucca application={self.api_token}',  # Maintenir le préfixe 'lucca application='
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
        """
        endpoint = f'{self.base_url}/api/v3/users'
        params = params or {}
        params['formerEmployees'] = 'true'
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            self.logger.info(f"Requête GET {response.url} - Statut: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                # Vérifier si la réponse contient un message d'erreur
                if 'message' in data:
                    self.logger.error(f"Erreur dans la réponse : {data['message']}")
                    if data['message'].lower() == "rate limit exceeded":
                        self.logger.error("Limite de taux atteinte.")
                    return []

                # Extraire 'items' de 'data'
                users = data.get('data', {}).get('items', [])
                return users

            elif response.status_code == 429:
                self.logger.error("Limite de taux atteinte (HTTP 429).")
                return []

            else:
                response.raise_for_status()

        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f'Erreur HTTP lors de la récupération des utilisateurs : {http_err}')
            return []

        except Exception as err:
            self.logger.error(f'Erreur lors de la récupération des utilisateurs : {err}')
            return []

    def get_departments(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Récupère la liste des départements depuis l'API Lucca.
        """
        endpoint = f'{self.base_url}/api/v3/departments'
        params = params or {}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            self.logger.info(f"Requête GET {response.url} - Statut: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                # Vérifier si la réponse contient un message d'erreur
                if 'message' in data:
                    self.logger.error(f"Erreur dans la réponse : {data['message']}")
                    if data['message'].lower() == "rate limit exceeded":
                        self.logger.error("Limite de taux atteinte.")
                    return []

                # Extraire 'items' de 'data'
                departments = data.get('data', {}).get('items', [])

                if not isinstance(departments, list):
                    self.logger.error("Le champ 'data' ou 'items' n'est pas une liste.")
                    return []

                return departments

            elif response.status_code == 429:
                self.logger.error("Limite de taux atteinte (HTTP 429).")
                return []

            else:
                response.raise_for_status()

        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f'Erreur HTTP lors de la récupération des départements : {http_err}')
            return []

        except Exception as err:
            self.logger.error(f'Erreur lors de la récupération des départements : {err}')
            return []
