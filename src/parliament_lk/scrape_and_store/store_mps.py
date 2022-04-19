import os

from utils import jsonx, timex, www

from parliament_lk._utils import log
from parliament_lk.scrape_and_store import scrape_mp, scrape_mp_dir
from utils_future.gitx import Git

URL_GIT = 'https://github.com/nuuuwan/parliament_lk'
DIR_GIT_DATA = '/tmp/parliament_lk.data'
DIR_MP_INFO = os.path.join(DIR_GIT_DATA, 'mp_info')
DIR_MP_IMAGES = os.path.join(DIR_GIT_DATA, 'mp_images')
GIT_UPLOAD_FREQUENCY = 10


def git_download():
    git = Git(URL_GIT, 'data', DIR_GIT_DATA)
    git.clone_and_checkout()

    if not os.path.exists(DIR_MP_INFO):
        os.mkdir(DIR_MP_INFO)

    if not os.path.exists(DIR_MP_IMAGES):
        os.mkdir(DIR_MP_IMAGES)
    return git


def git_upload(git):
    time_id = timex.get_time_id()
    message = f'[scrape_and_save] {time_id}'
    git.stage_commit_and_push(message)


def store_mp(mp_info):
    url_num = mp_info['url_num']
    mp_info_file = os.path.join(DIR_MP_INFO, f'{url_num}.json')
    jsonx.write(mp_info_file, mp_info)
    log.info(f'Stored mp {url_num} to {mp_info_file}')


def store_image(mp_info):
    url_num = mp_info['url_num']
    image_file = os.path.join(DIR_MP_IMAGES, f'{url_num}.jpg')

    if not os.path.exists(image_file):
        image_url = mp_info['image_url']
        www.download_binary(image_url, image_file)


def store_all():
    git = git_download()

    mp_dir_info_list = scrape_mp_dir.scrape_all()
    n_mps = len(mp_dir_info_list)
    for i, info in enumerate(mp_dir_info_list):
        log.debug(f'{i}/{n_mps}')
        url_num = info['url_num']
        mp_info = scrape_mp.scrape(url_num)
        store_mp(mp_info)
        store_image(mp_info)
        if i % GIT_UPLOAD_FREQUENCY == 0:
            git_upload(git)
        break

    git_upload(git)
    git.cleanup()


if __name__ == '__main__':
    store_all()
