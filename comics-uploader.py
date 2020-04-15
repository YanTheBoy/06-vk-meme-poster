import requests
import os
from dotenv import load_dotenv
import random


def get_request(link):
    response = requests.get(link)
    if response.ok:
        return response.json()


def fetch_pictures(response):
    """Function saved picture. Also return pic description and pic name"""
    alt = response['alt']
    picname = response['img'].split('/')[-1]
    response = requests.get(response['img'])
    if response.ok:
        with open(picname, 'wb') as file:
            file.write(response.content)
        return {
            'name': picname,
            'description': alt
        }


def get_upload_server(vk_api_url, main_params):
    method = 'photos.getWallUploadServer'
    response = requests.get('{}/{}'.format(vk_api_url, method), params=main_params)
    if response.ok:
        return response.json()


def upload_on_wall(server, picname):
    with open(picname, 'rb') as file:
        upload_url = server['response']['upload_url']
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
        if response.ok:
            return response.json()


def save_photo(loaded_photo, vk_api_url, main_params):
    method = 'photos.saveWallPhoto'
    params = {
        'access_token': main_params['access_token'],
        'v': main_params['v'],
        'server': loaded_photo['server'],
        'photo': loaded_photo['photo'],
        'hash': loaded_photo['hash']
    }
    response = requests.post('{}/{}'.format(vk_api_url, method), params=params)
    if response.ok:
        return response.json()


def make_wall_post(photo, vk_api_url, main_params, msg):
    method = 'wall.post'
    owner = photo['response'][0]['owner_id']
    media_id = photo['response'][0]['id']
    params = {
        'access_token': main_params['access_token'],
        'v': main_params['v'],
        'owner_id': -101830118,
        'from_group': 1,
        'message': msg,
        'attachments': 'photo{}_{}'.format(owner, media_id)
    }
    response = requests.get('{}/{}'.format(vk_api_url, method), params=params)
    if response.ok:
        return response.json()


if __name__ == '__main__':
    load_dotenv()
    access_token = os.getenv('VK_ACCESS_TOKEN')

    url = 'https://xkcd.com/info.0.json'
    xkcd_response = get_request(url)
    total_comics = xkcd_response['num']
    pic_number = random.choice(range(total_comics))
    picture = fetch_pictures(get_request('https://xkcd.com/{}/info.0.json'.format(pic_number)))

    vk_api = 'https://api.vk.com/method/'
    vk_main_params = {
        'access_token': access_token,
        'v': 5.103
    }
    upload_server = get_upload_server(vk_api, vk_main_params)
    uploaded_photo = upload_on_wall(upload_server, picture['name'])
    saved_photo = save_photo(
        uploaded_photo,
        vk_api,
        vk_main_params
    )
    posted_photo = make_wall_post(
        saved_photo,
        vk_api,
        vk_main_params,
        picture['description']
    )

    os.remove(picture['name'])
