import os
import urllib.request
import sys


def main():
    gelbooru = 'https://gelbooru.com/index.php?page=post&s='
    img_list = {}
    dwn_list = {}
    img_downloaded = 0
    platform = 1
    dwnbar_length = 20
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
# request settings
        req = urllib.request.Request(
            url=host,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        try:
            with urllib.request.urlopen(host) as page:
                page = page.read().decode()
        except urllib.error.HTTPError as err:
            print(err)
            result(img_downloaded)
# tag exisisting 
        p = page.find('Nobody here but us chickens!')
        if p != -1:
            print('Nothing found.')
            result(img_downloaded)
        page = page.split('<span id="s')
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
# remove duplicates
        for i in range(len(storage)):
            name = storage[i].split('.')
            name = name[0].split('_')
            if len(name) == 2:
                storage[i] = name[1]
            else:
                storage[i] = name[0]
        for key in img_list:
            name = img_list[key].split('.')
            if name[0] not in storage:
                dwn_list[key] = img_list[key]
        input('~{} files will be downloaded...'.format(len(dwn_list)))
# initiate progress bar
        sys.stdout.write("Downloading [{}]".format(" "*dwnbar_length))
        sys.stdout.flush()
        sys.stdout.write("\b"*(dwnbar_length+1))
        percent = len(dwn_list) / 100
# download new images
        for key in dwn_list:
            host = gelbooru+'view&id='+key
            try:
                with urllib.request.urlopen(req) as page:
                    page = page.read().decode()
            except urllib.error.HTTPError as err:
                print(err)
                result(img_downloaded)
            p = page.find('This post was deleted')
            if p == -1:
                page = page.split('src="//')
                link = page[2][0:page[2].find('"')]
                filename = link.split('/')[-1]
                filename = filename.split('?')
                filename = filename[0]
                urllib.request.urlretrieve('https://'+link, 'img/'+filename)
                img_downloaded += 1
                progress = str(round(img_downloaded / percent) / 5).split('.')
                progress = int(progress[0])
                sys.stdout.write("█"*progress)
                sys.stdout.flush()
                sys.stdout.write("\b"*progress)
    result(img_downloaded)

def result(img_downloaded):
    print('\nTask done! {} images downloaded'.format(img_downloaded))
    sys.exit()

def folder_init():
    try:
        os.mkdir('img')
    except FileExistsError:
        pass

if __name__ == '__main__':
    main()