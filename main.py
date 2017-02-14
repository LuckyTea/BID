import os
import time
import urllib.request

hostname = 'http://danbooru.donmai.us/'


def main():
    img_list = []
    url_list = []
    img_downloaded = 0
    try:
        f = urllib.request.urlopen(hostname)
    except urllib.error.HTTPError as err:
        print(err)
        exit()
    f = f.read()
    f = f.decode(encoding='UTF-8')
    f = f.split('<div id="posts">')
    f = f[1].split('<div class="paginator">')
    f = f[0].split('<article')
    f.remove('\n  <div style="overflow: hidden;">\n    ')
    folder_init()
    # take list of images from front page
    for i in f:
        k = i[61:68]
        img_list.append(k)
    # download each image from list
    for i in img_list:
        time.sleep(1)
        f = urllib.request.urlopen('http://danbooru.donmai.us/posts/'+i)
        f = f.read()
        f = f.decode(encoding='UTF-8')
        src_s = f.find('data-file-url="/data/__')
        src_e = f[src_s:].find('g"')
        link = hostname+f[src_s+16:src_s+src_e+1]
        filename = link.split('/')[-1]
        if filename not in os.listdir('img'):
            urllib.request.urlretrieve(link, 'img/'+filename)
            img_downloaded += 1
    # yay!
    print('Task done! {} images downloaded'.format(img_downloaded))


def folder_init():
    try:
        os.mkdir('img')
    except FileExistsError:
        pass

if __name__ == '__main__':
    main()
