import os
import time
import urllib.request
import sys


def main():
    gelbooru = 'https://gelbooru.com/index.php?page=post&s='
    img_list = []
    img_downloaded = 0
    print('BID launced.\n1. Gelbooru\n0. All\nChose platform:')
    while True:
        try:
            platform = int(input())
            break
        except TypeError:
            pass
    if platform == 1 or 0:
        try:
            page = urllib.request.urlopen(gelbooru+'list')
        except urllib.error.HTTPError as err:
            print(err)
            sys.exit()
        page = page.read().decode()
        page = page.split('<span class="yup">')
        page = page[1].split('<span id="s')
        folder_init()
# take list of images from the front page
        for i in page:
            id = i[0:7]
            img_list.append(id)
        img_list.pop(0)
# download each image from list
        for i in img_list:
            time.sleep(1)
            page = urllib.request.urlopen(gelbooru+'view&id='+i)
            page = page.read().decode()
            page = page.split('src="//')
            link = page[2][0:page[2].find('"')]
            filename = link.split('/')[-1]
            filename = filename.split('?')
            if filename[0] not in os.listdir('img'):
                urllib.request.urlretrieve('https://'+link, 'img/'+filename[0])
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
