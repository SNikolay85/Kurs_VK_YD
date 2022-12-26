import requests
from time import *
from tqdm import tqdm
import json

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token):
        self.params = {
            'access_token': token,
            'v': 5.131
        }

    def get_photos_count(self, vk_id, album):
        photos_get_url = self.url + 'photos.get'
        params = {
            'owner_id' : vk_id,
            'album_id' : album,
            'rev' : 0,
            'extended' : 1,
            'photo_sizes' : 0,
            'count' : 500
        }
        response = requests.get(photos_get_url, params={**self.params, **params}).json()
        return response['response']['count']

    def get_photos_name(self, vk_id, album, count_foto, list_names, list_data, list_size):
        photos_get_url = self.url + 'photos.get'
        params = {
            'owner_id' : vk_id,
            'album_id' : album,
            'rev' : 0,
            'extended' : 1,
            'photo_sizes' : 0,
            'count' : count_foto
        }
        response = requests.get(photos_get_url, params={**self.params, **params}).json()

        sizes = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm','s']
        max_index = 9
        for foto in response['response']['items']:
            for size in foto['sizes']:
                if size['type'] in sizes:
                    index = sizes.index(size['type'])
                    if max_index > index:
                        max_index = index
                        link = size['url']
                        s = size['type']
            max_index = 9
            if f"{foto['likes']['count']}.jpg" not in list_names.keys():
                list_names[f"{foto['likes']['count']}.jpg"] = link
                list_size['file_name'] = f"{foto['likes']['count']}.jpg"
                list_size['size'] = s

            else:
                result = localtime(foto['date'])
                list_names[f"{foto['likes']['count']}_{result.tm_mday}-{result.tm_mon}-{result.tm_year}.jpg"] = link
                list_size['file_name'] = f"{foto['likes']['count']}_{result.tm_mday}-{result.tm_mon}-{result.tm_year}.jpg"
                list_size['size'] = s
            d = list_size.copy()
            list_data.append(d)

class YaUploader:
    host = 'https://cloud-api.yandex.net/'

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        headers = {'Authorization': f'OAuth {self.token}'}
        return headers

    def get_folder(self, name_folder):
        uri = 'v1/disk/resources/'
        url = self.host + uri
        params = {'path': f'/{name_folder}'}
        response = requests.put(url, headers=self.get_headers(), params=params)

    def load(self, file_name, file_url, name_folder):
        uri = 'v1/disk/resources/upload/'
        url = self.host + uri
        params = {'path': f'/{name_folder}/{file_name}', 'url': file_url}
        response = requests.post(url, headers=self.get_headers(), params=params)

if __name__ == '__main__':
    token_YD = '*********************'
    token = '******************'
    downloader = VkUser(token)
    uploader = YaUploader(token_YD)

    user_id = input('Введи id пользователя: ')
    album = input('Откуда скачивать фото (profile/wall): ')
    if album == 'profile':
        text = 'в профиле'
    elif album == 'wall':
        text = 'на стене'
    print(f"Всего фото {text}: {downloader.get_photos_count(user_id, album)}")
    name_folder = input('При копировании фото, будет создана новая папка, введи её название: ')
    uploader.get_folder(name_folder)
    count_foto = int(input('Введи количество фотографий: '))
    list_names = {}
    list_data = []
    list_size = {'file_name': '', 'size': ''}

    downloader.get_photos_name(user_id, album, count_foto, list_names, list_data, list_size)

    for name, link in tqdm(list_names.items()):
        sleep(1)
        uploader.load(name, link, name_folder)
    data = list_data
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)

