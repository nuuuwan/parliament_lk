import os
import shutil

from utils import timex, tsv

from parliament_lk import scrape_mem, scrape_mem_dir
from parliament_lk._utils import log

URL_GIT = 'https://github.com/nuuuwan/parliament_lk'
if __name__ == '__main__':
    mem_dir_info_list = scrape_mem_dir.scrape_all()
    member_info_list = []
    for info in mem_dir_info_list:
        url_num = info['url_num']
        member_info = scrape_mem.scrape(url_num)
        member_info_list.append(member_info)

    dir_data = '/tmp/parliament_lk.data'
    if os.path.exists(dir_data):
        shutil.rmtree(dir_data)
    os.system(f'git clone {URL_GIT} {dir_data}')
    os.system(' &&'.join([
        f'cd {dir_data}',
        'git checkout data',
    ]))

    member_info_file = os.path.join(dir_data, 'member_info.tsv')
    tsv.write(member_info_file, member_info_list)
    log.info(f'Saved {member_info_file}')

    n_members = len(member_info_list)
    time_id = timex.get_time_id()
    message = f'[scrape_and_save] Added {n_members} MPs ({time_id})'

    os.system(' &&'.join([
        f'cd {dir_data}',
        'git add .',
        f'git commit -m "{message}"',
        'git push origin data',
    ]))
    shutil.rmtree(dir_data)
