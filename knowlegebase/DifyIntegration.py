import requests
import os
import yaml
import json
class DifyIntegration():
    def __init__(self, dataset_id,  config_path='config.yaml'):
        self.config = self.load_config(config_path)
        self.api_key = os.getenv('DIFY_API_KEY')
        if self.api_key is None:
            raise ValueError("DIFY_API_KEY environment variable not set.")
        self.dataset_id = dataset_id
        self.base_url = self.config.get('base_url_dify')

    def add_document(self, document):
        url = f"{self.base_url}/datasets/{self.dataset_id}/document/create_by_text"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"text": document}
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    """
    上传文档到指定的数据集中。

    该方法通过POST请求将本地文档上传到远程服务器。它首先准备上传所需的URL和请求头，
    然后根据提供的文档路径和文件类型获取文件，并将其作为二进制数据上传。

    参数:
    - document_path (str): 本地文档的路径。
    - file_type (str): 文件的类型，用于确定MIME类型。

    返回:
    - dict: 服务器返回的响应，以JSON格式解析。
    """

    def upload_document(self, dataset_id, document_path, file_type):
        url = f"{self.base_url}/datasets/{dataset_id}/document/create_by_file"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"File '{document_path}' does not exist.")
        file_name = os.path.basename(document_path)
        mime_type = self.get_mime_type(file_name, file_type)
        with open(document_path, 'rb') as file:
            datatemp = {
                'indexing_technique': 'high_quality',
                'process_rule': {
                    "mode": "custom",
                    'rules': {
                        'pre_processing_rules': [
                            {'id': 'remove_extra_spaces', 'enabled': True},
                            {'id': 'remove_urls_emails', 'enabled': True}
                        ],
                        'segmentation': {
                            'separator': '###',
                            'max_tokens': 500
                        },
                   },
                }
            }
            # 将 JSON 数据转换为字符串
            json_data = json.dumps(datatemp)
            files = {
                #'data': (None, json_data, 'application/json'),
                'file': (file_name, file, mime_type)
            }
            data = {'data': (None, json_data, 'application/json'),}
            response = requests.post(url, headers=headers, data=data, files=files)
            return response.json()

    def get_mime_type(self, file_name, file_type):
        # 根据文件扩展名和指定的文件类型返回 MIME 类型
        extension = file_name.split('.')[-1].lower()
        mime_types = {
            'txt': 'text/plain',
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'png': 'image/png',
            'csv': 'text/csv',
            'md': 'text/markdown',
            # 添加其他文件类型及其对应的 MIME 类型
        }
        return mime_types.get(extension, file_type)  # 默认使用传入的 file_type


    def delete_document(self, document_id):
        url = f"{self.base_url}/datasets/{self.dataset_id}/documents/{document_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.delete(url, headers=headers)
        return response.json()

    def load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as fin:
            configs = yaml.load(fin, Loader=yaml.FullLoader)
            return configs