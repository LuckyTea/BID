import os
import time
import urllib.request
import sys


def main():
    gelbooru = 'https://gelbooru.com/index.php?page=post&s='
    img_list = {}
    img_downloaded = 0
    print('BID launced.\n1. Gelbooru\n0. All')
    while True:
        try:
            platform = int(input('Chose platform: '))
            break
        except TypeError:
            pass
    if platform == 1 or platform == 0:
        tags = input('Tags separated by comma: ').lower()
        if len(tags) < 1:
            tags = tags.split(',')
            for i in range(len(tags)):
                for a in range(len(tags[i])): 
                    if tags[i][a] not in [' ']:
                        tags[i] = tags[i][a:]
                        break
                    else:
                        pass
                tags[i] = tags[i].replace(' ', '_')
            tags = '+'.join(tags)
            host = gelbooru+'list&tags='+tags
        else:
            host = gelbooru+'list'
        try:
            page = urllib.request.urlopen(host)
        except urllib.error.HTTPError as err:
            print(err)
            sys.exit()
        page = page.read().decode()
        page = page.split('<span class="yup">')
        page = page[1].split('<span id="s')
        page.pop(0)
# take information
        for i in page:
            id = i.split('"')
            id = id[0]
            filename = i.split('img src="')
            filename = filename[1].split('?')
            filename = filename[0].split('/')
            filename = filename[-1].split('_')
            filename = filename[1]
            img_list[id] = filename
        folder_init()
        storage = os.listdir('img')
# download new images
        for key in img_list:
            if img_list[key] in storage:
                pass
            else:
                time.sleep(0.75)
                page = urllib.request.urlopen(gelbooru+'view&id='+key)
                page = page.read().decode()
                page = page.split('src="//')
                link = page[2][0:page[2].find('"')]
                urllib.request.urlretrieve('https://'+link, 'img/'+img_list[key])
                img_downloaded += 1
# yay!
    print('Task done! {} images downloaded'.format(img_downloaded))
    sys.exit()


def folder_init():
    try:
        os.mkdir('img')
    except FileExistsError:
        pass

if __name__ == '__main__':
    main()
