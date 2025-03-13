import requests
from knowlegebase.db_operations import KnowledgeBase
import os
class RagFlowIntegration(KnowledgeBase):
    def __init__(self, knowledge_base_id, config_path='config.yaml'):
        self.config = self.load_config(config_path)
        self.api_key = os.getenv('RAGFLOW_API_KEY')
        if self.api_key is None:
            raise ValueError("RAGFLOW_API_KEY environment variable not set.")
        self.api_url = self.config.get('base_url_ragflow')
        self.knowledge_base_id = knowledge_base_id

    def add_document(self, document):
        url = f"{self.api_url}/knowledge_bases/{self.knowledge_base_id}/documents"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"document": document}
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def update_document(self, document_id, new_data):
        url = f"{self.api_url}/knowledge_bases/{self.knowledge_base_id}/documents/{document_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"document": new_data}
        response = requests.put(url, headers=headers, json=data)
        return response.json()

    def delete_document(self, document_id):
        url = f"{self.api_url}/knowledge_bases/{self.knowledge_base_id}/documents/{document_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.delete(url, headers=headers)
        return response.json()