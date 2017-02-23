import os
import urllib.request
import sys


def main():
    gelbooru = 'https://gelbooru.com/index.php?page=post&s='
    img_list = {}
    dwn_list = {}
    img_downloaded = 0
    platform = 1
    '''
    print('BID launced.\n1. Gelbooru\n0. All')
    while True:
        try:
            platform = int(input('Chose platform: '))
            break
        except TypeError:
            pass
    '''
    if platform == 1 or platform == 0:
        tags = input('Tags separated by comma: ').lower()
        if len(tags) > 1:
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
            page = urllib.request.urlopen(host).read().decode()
        except urllib.error.HTTPError as err:
            print(err)
            result(img_downloaded)
# tag exisisting 
        p = page.find('Nobody here but us chickens!')
        if p != -1:
            print('Nothing found.')
            result(img_downloaded)
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
        for i in range(len(storage)):
            name = storage[i].split('.')
            name = name[0].split('_')
            if len(name) == 2:
                storage[i] = name[1]
            else:
                storage[i] = name[0]
# remove duplicates
        for key in img_list:
            name = img_list[key].split('.')
            if name[0] not in storage:
                dwn_list[key] = img_list[key]
        input('~{} elements will be downloaded...'.format(len(dwn_list)))
# download new images
        for key in dwn_list:
            page = urllib.request.urlopen(gelbooru+'view&id='+key).read().decode()
            p = page.find('This post was deleted')
            if p == -1:
                page = page.split('src="//')
                link = page[2][0:page[2].find('"')]
                filename = link.split('/')[-1]
                filename = filename.split('?')
                filename = filename[0]
                urllib.request.urlretrieve('https://'+link, 'img/'+filename)
                img_downloaded += 1
    result(img_downloaded)

def result(img_downloaded):
    print('Task done! {} images downloaded'.format(img_downloaded))
    sys.exit()

def folder_init():
    try:
        os.mkdir('img')
    except FileExistsError:
        pass

if __name__ == '__main__':
    main()