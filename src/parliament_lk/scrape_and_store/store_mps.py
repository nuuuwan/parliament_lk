import os
import threading

from utils import jsonx, mr, timex, tsv, www

from parliament_lk._constants import URL_GIT
from parliament_lk._utils import log
from parliament_lk.scrape_and_store import scrape_mp, scrape_mp_idx
from utils_future.gitx import Git

DIR_GIT_DATA = '/tmp/parliament_lk.data'
DIR_MP_INFO = os.path.join(DIR_GIT_DATA, 'mp_info')
DIR_MP_IMAGES = os.path.join(DIR_GIT_DATA, 'mp_images')
GIT_UPLOAD_FREQUENCY = 10
MAX_THREADS = 3

MP_LIST_JSON_FILE = os.path.join(DIR_GIT_DATA, 'mp_list.json')
MP_LIST_FILE = os.path.join(DIR_GIT_DATA, 'mp_list.tsv')


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
    message = f'[store_mps] {time_id}'
    git.stage_commit_and_push(message)


def scrape_and_store_mp_idx(FORCE_SCRAPE):
    mp_idx_file = os.path.join(DIR_GIT_DATA, 'mp_idx.tsv')
    if not FORCE_SCRAPE and os.path.exists(mp_idx_file):
        return tsv.read(mp_idx_file)

    mp_idx_info_list = scrape_mp_idx.scrape_all_indices()
    tsv.write(mp_idx_file, mp_idx_info_list)
    log.info(f'Stored {mp_idx_file}')
    return mp_idx_info_list


def scrape_and_store_mp(url_num, FORCE_SCRAPE):
    mp_info_file = os.path.join(DIR_MP_INFO, f'{url_num}.json')
    if not FORCE_SCRAPE and os.path.exists(mp_info_file):
        return jsonx.read(mp_info_file)

    mp_info = scrape_mp.scrape(url_num)
    jsonx.write(mp_info_file, mp_info)
    log.info(f'Stored mp {url_num} to {mp_info_file}')
    return mp_info


def download_and_store_image(mp_info, FORCE_SCRAPE):
    url_num = mp_info['url_num']
    image_file = os.path.join(DIR_MP_IMAGES, f'{url_num}.jpg')
    if not FORCE_SCRAPE and os.path.exists(image_file):
        return

    image_url = mp_info['image_url']
    www.download_binary(image_url, image_file)


def store_all(FORCE_SCRAPE):
    git = git_download()
    mp_idx_info_list = scrape_and_store_mp_idx(FORCE_SCRAPE)
    git_upload(git)

    n_mps = len(mp_idx_info_list)
    git_lock = threading.Lock()

    def store_all_item(i, info):
        log.debug(f'{i}/{n_mps}')
        url_num = info['url_num']
        mp_info = scrape_and_store_mp(url_num, FORCE_SCRAPE)
        download_and_store_image(mp_info, FORCE_SCRAPE)

        if i % GIT_UPLOAD_FREQUENCY == 0:
            git_lock.acquire()
            git_upload(git)
            git_lock.release()

        return mp_info

    mp_info_list = mr.map_parallel(
        lambda x: store_all_item(x[0], x[1]),
        enumerate(mp_idx_info_list),
        MAX_THREADS,
    )

    jsonx.write(MP_LIST_JSON_FILE, mp_info_list)
    log.info(f'Stored {n_mps} items {MP_LIST_JSON_FILE}')

    os.path.join(DIR_GIT_DATA, 'mp_list.tsv')
    tsv.write(MP_LIST_FILE, mp_info_list)
    log.info(f'Stored {n_mps} items {MP_LIST_FILE}')

    git_upload(git)
