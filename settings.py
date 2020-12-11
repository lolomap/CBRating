# coding=utf-8
DEBUG = False

DIRECTORIES = {}
if not DEBUG:
    DIRECTORIES['list'] = 'LIST_DIRECTORY'
    DIRECTORIES['data'] = 'DATA_DIRECTOTY'
    DIRECTORIES['long_data'] = 'LONG_DATA_DIRECTOTY'
    DIRECTORIES['photo'] = 'PLOT_IMAGE_DIRECTOTY'
    DIRECTORIES['inf_photo'] = 'INF_IMAGE_DIRECTOTY'
    DIRECTORIES['k_photo'] = 'K_IMAGE_DIRECTOTY'
else:
    DIRECTORIES['list'] = 'list.txt'
    DIRECTORIES['data'] = 'data.txt'
    DIRECTORIES['long_data'] = 'long_data.txt'
    DIRECTORIES['photo'] = 'plot_image'
    DIRECTORIES['inf_photo'] = 'inf_image'
    DIRECTORIES['k_photo'] = 'k_image'

login, password = 'PHONE NUMBER', 'PASSWORD'
token = 'TOKEN'
if not DEBUG:
    our_id = 0 # GROUP ID
else:
    our_id = 0 # GROUP ID
