from abc import ABC, abstractmethod

class KnowledgeBase(ABC):
    def __init__(self, config_path='config.yaml'):
        self.config = self.load_config(config_path)
    @abstractmethod
    def add_document(self, document):
        pass

    @abstractmethod
    def update_document(self, document_id, new_data):
        pass

    @abstractmethod
    def delete_document(self, document_id):
        pass