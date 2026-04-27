import time, requests, json, logging
from settings import yd_token
from urllib.parse import quote

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class YD:
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'OAuth {token}'}
        self.baze_url = 'https://cloud-api.yandex.net'

    def create_folder(self, folder_name):
        self.folder_name = folder_name
        return requests.put(f'{self.baze_url}/v1/disk/resources',
                                 headers=self.headers, params={'path': self.folder_name})
    
    def delete_folder(self, folder_name):
        self.folder_name = folder_name
        return requests.delete(f'{self.baze_url}/v1/disk/resources',
                                 headers=self.headers, params={'path': self.folder_name})
    
    def upload_file_by_url(self, file_url, file_name):
        self.file_url, self.file_name = file_url, file_name
        return requests.post(f'{self.baze_url}/v1/disk/resources/upload',
                                 headers=self.headers, params={'path': self.file_name, 'url': self.file_url})

    
    def get_file_metadata(self, file_name):
        logging.info(f'Get file metadata: {file_name}')
        return requests.get(f'{self.baze_url}/v1/disk/resources',
                            headers=self.headers,params={'path': file_name})

def save_size_to_json(yd, file_path, json_file_name):
    response = yd.get_file_metadata(file_path)
    response.raise_for_status()
    data = response.json()
    file_info = {"file_name": file_path, "size": data["size"]}
    with open(json_file_name, "w", encoding="utf-8") as file:
        json.dump(file_info, file, indent=4, ensure_ascii=False)
    logging.info(f'File {file_path} with size {data["size"]} saved to JSON {json_file_name}')

def upload_cat_to_yd(yd, text, folder_name='Python148'):
    logging.info(f'Create folder {folder_name} to YD')
    yd.create_folder(folder_name)
    logging.info('Upload cat to YD')
    yd.upload_file_by_url(f"https://cataas.com/cat/cute/says/{quote(text)}", f'{folder_name}/{text}.jpg')
    time.sleep(10)
    save_size_to_json(yd, f'{folder_name}/{text}.jpg', 'file_size.json')


if __name__ == '__main__':
    yd = YD(yd_token)
    text = input('Enter text: ')
    upload_cat_to_yd(yd, text)
