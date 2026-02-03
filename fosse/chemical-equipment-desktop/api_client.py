import requests
import json
import base64

class APIClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIClient, cls).__new__(cls)
            cls._instance.base_url = 'http://localhost:8000/api'
            cls._instance.access_token = None
            cls._instance.user_data = None
        return cls._instance

    def login(self, username, password):
        try:
            response = requests.post(f"{self.base_url}/auth/login/", 
                                   json={"username": username, "password": password})
            data = response.json()
            if response.status_code == 200:
                self.access_token = data.get('access')
                self.user_data = data.get('user')
                return True, "Login successful"
            return False, data.get('error', 'Login failed')
        except Exception as e:
            return False, str(e)

    def google_login(self, email):
        """Quick demo login matching web behavior"""
        try:
            response = requests.post(f"{self.base_url}/auth/google/", 
                                   json={"email": email})
            data = response.json()
            if response.status_code == 200:
                self.access_token = data.get('access')
                self.user_data = data.get('user')
                return True, "Demo login successful"
            return False, data.get('error', 'Login failed')
        except Exception as e:
            return False, str(e)

    def get_headers(self):
        headers = {}
        if self.access_token:
            headers['Authorization'] = f"Bearer {self.access_token}"
        return headers

    def upload_csv(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.base_url}/upload/", 
                                       headers=self.get_headers(),
                                       files=files)
            data = response.json()
            if response.status_code == 201:
                return True, data
            return False, data.get('error', 'Upload failed')
        except Exception as e:
            return False, str(e)

    def get_history(self):
        try:
            response = requests.get(f"{self.base_url}/history/", 
                                  headers=self.get_headers())
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []

    def get_equipment_data(self, dataset_id=None):
        try:
            params = {"dataset_id": dataset_id} if dataset_id else {}
            response = requests.get(f"{self.base_url}/data/", 
                                  headers=self.get_headers(),
                                  params=params)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception:
            return []

    def get_statistics(self, dataset_id=None):
        try:
            params = {"dataset_id": dataset_id} if dataset_id else {}
            response = requests.get(f"{self.base_url}/stats/", 
                                  headers=self.get_headers(),
                                  params=params)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception:
            return None
