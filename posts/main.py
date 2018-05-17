import requests
from os import environ

"""
https://developers.facebook.com/docs/graph-api/reference/v3.0/post

https://developers.facebook.com/tools/explorer/
export ACCESS_TOKEN=
"""

def get_page_id(page_name):
    url = '{}/{}'.format(graph_api_prefix, page_name)
    params = {
        'access_token': token
    }
    try:
        res = requests.get(url=url, params=params)
    except Exception as e:
        print('Error:')
        print(e)
    return res.json()

def get_page_posts(page_id):
    url = '{}/{}/posts'.format(graph_api_prefix, page_id)
    params = {
        'access_token': token
    }
    try:
        res = requests.get(url=url, params=params)
    except Exception as e:
        print('Error:')
        print(e)
    return res.json()

graph_api_prefix = 'https://graph.facebook.com/v3.0'
token = environ['ACCESS_TOKEN']

page_id = get_page_id('appledaily.tw')['id']
data = get_page_posts(page_id)['data']
for d in data:
    print(d['message'])
