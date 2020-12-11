# coding=utf-8
from sys import argv
import vk

DEBUG = False
DIRECTORIES = {}
if not DEBUG:
    DIRECTORIES['list'] = 'LIST_DIRECTORY'
    DIRECTORIES['long_data'] = 'LONG_DATA_DIRECTORY'
else:
    DIRECTORIES['list'] = 'list.txt'
    DIRECTORIES['long_data'] = 'long_data.txt'

try:
    login, password = 'PHONE NUMBER', 'PASSWORD'
    token = 'TOKEN'
    session = vk.Session(access_token=token)
    vk_api = vk.API(session)

    name_list = ''
    for arg in argv[1:]:
        name_list = name_list + '\n' + arg
    list_file = open(DIRECTORIES['list'], 'a')
    list_file.write(name_list)
    list_file.close()

    g_l = argv[1:]
    for g in g_l:
        if g[:3] == 'id:':
            g = int(g[3:])

    id_list = ''

    for group in vk_api.groups.getById(group_ids=g_l, v='5.73'):
        id_list = id_list + str(group['id']) + '=None\n'

    file = open(DIRECTORIES['long_data'], 'r')
    data = file.read()
    file.close()
    data = data.replace('**SECTION**\n', '**SECTION**\n'+id_list)
    file = open(DIRECTORIES['long_data'], 'w')
    file.write(data)
    file.close()
    print('\n\n***SUCCESS***\n')
except Exception as e:
    print('\n\n***ERROR!!!!***\n'+e.__str__())

