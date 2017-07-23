import asyncio
import os
import re
import requests

async def download_coroutine(url):
    await asyncio.sleep(.5)
    # get img link
    response = requests.get(url)
    content = response.content.decode('utf8')
    url = re.findall(r'<li><a href="(//gelbooru.com//[^"]*)"', content)
    url = f'https:{url[0]}'
    request = requests.get(url, stream=True)
    filename = os.path.basename(url)
    # get it!!1
    with open(filename, 'wb') as file:
        for chunk in request.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    print(f'{filename} downloaded')


def main():
    # get tags
    tags = (input('tags to download: ')).replace(' ', '+')
    req = f'https://gelbooru.com/index.php?page=post&s=list&tags={tags}'
    response = requests.get(req)
    content = response.content.decode('utf8')
    ids = re.findall(r'<div class="thumbnail-preview"><span id="s(\d+)" class="thumb">', content)
    # get all imgs from first page
    urls = []
    for i in ids:
        urls.append(f'https://gelbooru.com/index.php?page=post&s=view&id={i}')
    input(f'{len(urls)} elements to download')
    # initialize asyncio
    loop = asyncio.get_event_loop()
    coroutines = [download_coroutine(url) for url in urls]
    wait_coroutines = asyncio.wait(coroutines)
    try:
        loop.run_until_complete(wait_coroutines)
    finally:
        loop.close()
        print('Complete!')


if __name__ == '__main__':
    main()
