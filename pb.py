from sys import argv, exit
import pynb
from requests import get, exceptions as rex

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    title = False
    title_text = ''

    def handle_starttag(self, tag, attrs):
        if not self.title and tag == 'title':
            self.title =  True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.title =  False

    def handle_data(self, data):
        if self.title and not self.title_text:
            self.title_text = data

parser = MyHTMLParser()

def help(topic=None):
    if topic:
        print(f'{topic} help')
    else:
        print('general help')
    exit(1)

def get_title(url):
    try:
        r = get(url)
    except rex.SSLError as e:
        print(e)
        exit(1)
    mp = MyHTMLParser()
    mp.feed(r.text)
    return ' '.join(mp.title_text.split())

def get_tags(url):
    tags = pynb.posts_suggest(url)
    popular = tags['popular']
    return ' '.join(popular)

def add_url(url):
    title = get_title(url)
    print(f'title: {title}')
    tags = get_tags(url)
    print(f'tags:  {tags}')
    params={'tags': tags}
    description = ''
    if input('Add description? ').lower() == 'y':
        description = input('Description: ').strip()
    if description:
        params['extended'] = description
    pynb.posts_add(url, title, params=params)

if __name__ == "__main__":
    if len(argv) == 1:
        help()

    commands = {'add': add_url}

    if argv[1] not in commands:
        help()

    if len(argv) == 2:
        help(argv[1])

    url = ' '.join(argv[2:])
    command = commands[argv[1]]
    command(url)
    print(pynb.posts_get())