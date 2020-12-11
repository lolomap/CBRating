# coding=utf-8
import vk
import requests
import json
import time
from settings import token, our_id, DIRECTORIES

session = vk.Session(access_token=token)
vk_api = vk.API(session)


def get_groups_info(groups_id):
    return vk_api.groups.getById(group_ids=groups_id, fields='members_count', v='5.73')


def get_group_posts_count(owner_id, days):
    posts = vk_api.wall.get(owner_id=owner_id, count=100, v='5.37')
    count = 0
    likes = 0
    comments = 0
    for pst in posts['items']:
        if pst['date'] >= int(time.time()) - 86400*days:
            count = count + 1
            likes = likes + pst['likes']['count']
            comments = comments + pst['comments']['count']
    return {'count': count, 'likes': likes, 'comments': comments}


def upload_photo(name):
    photo_server = vk_api.photos.getWallUploadServer(group_id=our_id, v='5.73')
    upload_url = photo_server['upload_url']
    if name == 'plot':
        img = {'photo': ('plot_image.png', open(DIRECTORIES['photo'] + '.png', 'rb'))}
    elif name == 'inf':
        img = {'photo': ('inf_image.png', open(DIRECTORIES['inf_photo'] + '.png', 'rb'))}
    elif name == 'k':
        img = {'photo': ('k_image.png', open(DIRECTORIES['k_photo'] + '.png', 'rb'))}
    else:
        raise Exception('Wrong photo name')
    response = requests.post(upload_url, files=img)
    result = json.loads(response.text)
    photo = vk_api.photos.saveWallPhoto(photo=result['photo'],
                                        hash=result['hash'], server=result['server'], group_id=our_id, v='5.73')
    return 'photo'+str(photo[0]['owner_id'])+'_'+str(photo[0]['id'])


def post(text, photos):
    vk_api.wall.post(owner_id=-our_id, from_group=1, message=text,
                     attachments=photos, v='5.73')
