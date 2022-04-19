import os

from utils import jsonx, timex, www

from parliament_lk import scrape_mem, scrape_mem_dir
from parliament_lk._utils import log
from utils_future.gitx import Git

URL_GIT = 'https://github.com/nuuuwan/parliament_lk'
DIR_GIT_DATA = '/tmp/parliament_lk.data'
DIR_MEMBER_INFO = os.path.join(DIR_GIT_DATA, 'member_info')
DIR_MEMBER_IMAGES = os.path.join(DIR_GIT_DATA, 'member_images')
GIT_UPLOAD_FREQUENCY = 10


def git_download():
    git = Git(URL_GIT, 'data', DIR_GIT_DATA)
    git.clone_and_checkout()

    if not os.path.exists(DIR_MEMBER_INFO):
        os.mkdir(DIR_MEMBER_INFO)
    if not os.path.exists(DIR_MEMBER_IMAGES):
        os.mkdir(DIR_MEMBER_IMAGES)
    log.info('git_download: complete.')
    return git


def git_upload(git):
    time_id = timex.get_time_id()
    message = f'[scrape_and_save] {time_id}'
    git.stage_commit_and_push(message)
    log.info('git_upload: complete.')


def store_member(member_info):
    url_num = member_info['url_num']
    member_info_file = os.path.join(DIR_MEMBER_INFO, f'{url_num}.json')
    jsonx.write(member_info_file, member_info)
    log.info(f'Stored member {url_num} to {member_info_file}')


def store_image(member_info):
    url_num = member_info['url_num']
    image_file = os.path.join(DIR_MEMBER_IMAGES, f'{url_num}.jpg')

    if not os.path.exists(image_file):
        image_url = member_info['image_url']
        www.download_binary(image_url, image_file)


if __name__ == '__main__':
    git = git_download()

    mem_dir_info_list = scrape_mem_dir.scrape_all()
    n_members = len(mem_dir_info_list)
    for i, info in enumerate(mem_dir_info_list):
        log.debug(f'{i}/{n_members}')
        url_num = info['url_num']
        member_info = scrape_mem.scrape(url_num)
        store_member(member_info)
        store_image(member_info)
        if i % GIT_UPLOAD_FREQUENCY == 0:
            git_upload(git)

    git_upload(git)
    git.cleanup()
