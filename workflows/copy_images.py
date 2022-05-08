import os

from utils import logx

from parliament_lk._constants import URL_GIT
from utils_future.gitx import Git

DIR_GIT_DATA = '/tmp/parliament_lk.data'
DIR_IMAGES = os.path.join(DIR_GIT_DATA, 'mp_images')
DIR_JS_IMAGES = os.path.join(
    '/Users/nuwan.senaratna/Not.Dropbox',
    '_CODING/js_react',
    'parliament_lk_app',
    'public',
    'mp_images',
)

log = logx.get_logger('copy_images')


def main():
    DIR_GIT_DATA = '/tmp/parliament_lk.data'
    git = Git(URL_GIT, 'data', DIR_GIT_DATA)
    git.clone_and_checkout()
    os.system(f'cp {DIR_IMAGES}/* {DIR_JS_IMAGES}/')


if __name__ == '__main__':
    main()
