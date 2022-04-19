import os
import shutil

from utils import jsonx, timex

from parliament_lk import scrape_mem, scrape_mem_dir
from parliament_lk._utils import log

DIR_GIT_DATA = '/tmp/parliament_lk.data'
DIR_MEMBER_INFO = os.path.join(DIR_GIT_DATA, 'member_info')


def git_download():
    if os.path.exists(DIR_GIT_DATA):
        shutil.rmtree(DIR_GIT_DATA)
    os.system(f'git clone {URL_GIT} {DIR_GIT_DATA}')
    os.system(' &&'.join([
        f'cd {DIR_GIT_DATA}',
        'git checkout data',
    ]))

    if not os.path.exists(DIR_MEMBER_INFO):
        os.mkdir(DIR_MEMBER_INFO)


def git_upload(url_num):
    time_id = timex.get_time_id()
    message = f'[scrape_and_save] Added MP {url_num} ({time_id})'
    os.system(' &&'.join([
        f'cd {DIR_GIT_DATA}',
        'git add .',
        f'git commit -m "{message}"',
        'git push origin data',
    ]))


def store_member(member_info):
    url_num = member_info['url_num']
    member_info_file = os.path.join(DIR_MEMBER_INFO, f'{url_num}.json')
    jsonx.write(member_info_file, member_info)
    log.info(f'Stored MP {url_num} to {member_info_file}')


URL_GIT = 'https://github.com/nuuuwan/parliament_lk'
if __name__ == '__main__':
    git_download()

    mem_dir_info_list = scrape_mem_dir.scrape_all()
    n_members = len(mem_dir_info_list)
    for i, info in enumerate(mem_dir_info_list):
        url_num = info['url_num']
        member_info = scrape_mem.scrape(url_num)
        store_member(member_info)
        git_upload(url_num)

    shutil.rmtree(DIR_GIT_DATA)
