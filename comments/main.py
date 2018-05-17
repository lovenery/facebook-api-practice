import requests
from os import path, environ

"""
Refs:
https://developers.facebook.com/docs/graph-api/reference/v3.0/comment
https://developers.facebook.com/docs/graph-api/reference/v3.0/object/comments
Get all available fields: https://stackoverflow.com/questions/42633944/how-get-all-fields-api-graph-v2-8-of-facebook

Target: Crawl all comments and replies.
https://www.facebook.com/appledaily.tw/posts/10156769966527069

Graph api explorer to get ACCESS_TOKEN: https://developers.facebook.com/tools/explorer/
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

def store_comments_and_replies_to_csv(page_id, post_id, file_name):
    with open(file_name, 'w') as f:
        f.write('id,type,created_time,permalink_url,application_name,like_count,attachment_url,message' + '\n')

    next_url = '{}/{}_{}/comments'.format(graph_api_prefix, page_id, post_id)
    print('GET COMMENT BY POST :', next_url)
    fields = 'id,created_time,permalink_url,application,like_count,attachment,message,comment_count'
    params = {
        'access_token': token,
        'fields': fields
    }
    while True:
        try:
            res = requests.get(url=next_url, params=params)
            res = res.json()
        except Exception as e:
            print('Error:')
            print(e)

        comments = res['data']
        for comment in comments:
            application_name = None
            if ('application' in comment) == True:
                application_name = comment['application']['name']
            attachment_url = None
            if ('attachment' in comment) == True:
                attachment_url = comment['attachment']['url']
            s = '{},{},{},{},{},{},{},"{}"\n'.format(comment['id'], 'COMMENT', comment['created_time'], comment['permalink_url'], application_name, comment['like_count'], attachment_url, comment['message'].replace("\n", "\\n"))
            with open(file_name, 'a') as new_file:
                new_file.write(s)

            reply_count = comment['comment_count']
            if reply_count > 0:
                reply_url = '{}/{}/comments'.format(graph_api_prefix, comment['id'])
                print('GET REPLY BY COMMENT:', reply_url)
                try:
                    replies = requests.get(url=reply_url, params=params)
                    replies = replies.json()
                except Exception as e:
                    print('Error:')
                    print(e)

                replies = replies['data']
                for reply in replies:
                    application_name = None
                    if ('application' in reply) == True:
                        application_name = reply['application']['name']
                    attachment_url = None
                    if ('attachment' in reply) == True:
                        attachment_url = reply['attachment']['url']
                    s = '{},{},{},{},{},{},{},"{}"\n'.format(reply['id'], '  REPLY', reply['created_time'], reply['permalink_url'], application_name, reply['like_count'], attachment_url, reply['message'].replace("\n", "\\n"))
                    with open(file_name, 'a') as new_file:
                        new_file.write(s)

        if ('next' in res['paging']) == False:
            print('沒有下一頁了。')
            break
        next_url = res['paging']['next']

base_dir = path.abspath(path.dirname(__file__))
graph_api_prefix = 'https://graph.facebook.com/v3.0'
token = environ['ACCESS_TOKEN']

page_id = get_page_id('appledaily.tw')['id']
post_id = '10156769966527069'
file_name = path.join(base_dir, 'result.csv')
store_comments_and_replies_to_csv(page_id, post_id, file_name)
