from config import load_config

from requests import get
from sys import argv, exit
from datetime import datetime

import json

common = {
    'auth_token': 'name:token',
    'format': 'json'
}
common = load_config(common, config_name='pynb')

baseURL = 'https://api.pinboard.in/v1/'
cache_file = 'pb.json'


def make_request(endpoint, params=None):
    params = params if params else {}
    all_params = {**params, **common}

    path = f'{baseURL}{endpoint}'
    response = get(path, all_params)

    code = response.status_code
    if code != 200:
        print(dir(response))
        raise Exception(f'request failed with: {code}', code)
    data = json.loads(response.text)
    return data

def posts_update():
    response = make_request('posts/update')
    # ISO format except trailing 'Z'
    return datetime.fromisoformat(response['update_time'][:-1])

def posts_add(url, description, *, params=None):
    params = params if params else {}
    required_params = {'url': url, 'description': description} 
    all_params = {**params, **required_params}
    response = make_request('posts/add', all_params)
    return response['result_code']

def posts_delete(url):
    response = make_request('posts/delete', params={'url': url})
    return response['result_code']

def posts_get(*, params=None):
    params = params if params else {}
    response = make_request('posts/get', params)
    return response

def posts_dates():
    j_response = make_request('posts/dates')
    pass

def posts_recent():
    j_response = make_request('posts/recent')
    pass

def posts_all():
    response = make_request('posts/all')
    return response['result_code']

def posts_suggest(url): 
    response = make_request('posts/suggest', params={'url': url})
    return {'popular': response[0]['popular'], 
            'recommended': response[1]['recommended']}

def tags_get():
    response = make_request('tags/get')
    return response

def tags_delete(tag_name):
    response = make_request('tags/delete', params={'tag': tag_name})
    return response['result']

def tags_rename(old_tag, new_tag):
    response = make_request('tags/rename', params={'old': old_tag, 'new': new_tag})
    return response['result']

def user_secret():
    response = make_request('user/secret')
    return response['result']

def user_api_token():
    response = make_request('user/api_token')
    return response['result']

class Note:
    def __init__(self, id, title, length):
        self.id = id
        self.title = title
        self.length = length
        self.text = None
        self.hash = None
        self.created_at = None
        self.updated_at = None

    def __str__(self):
        if not self.text:
            note = notes_ID(self.id)
            self.text = note['text']
            self.hash = note['hash']
            self.created_at = note['created_at']
            self.updated_at = note['updated_at']

        return f'{self.title}\n\n{self.text}'

def notes_list():
    response = make_request('notes/list')
    notes = []
    for note in response['notes']:
        notes.append(Note(note['id'], note['title'], note['length']))
    return notes

def notes_ID(ID):
    response = make_request(f'notes/{ID}')
    return response

if __name__ == "__main__":
    print(posts_get(params={}))
