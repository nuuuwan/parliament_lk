import os
import shutil

from utils import timex
from utils.xmlx import _

from parliament_lk._constants import URL_GIT
from parliament_lk._utils import log
from parliament_lk.core import MP
from utils_future.gitx import Git

DIR_GIT_GH_PAGES = '/tmp/parliament_lk.gh-pages'
CSS_FILE = 'src/parliament_lk/render/styles.css'


def git_download():
    git = Git(URL_GIT, 'gh-pages', DIR_GIT_GH_PAGES)
    git.clone_and_checkout()
    return git


def git_upload(git):
    time_id = timex.get_time_id()
    message = f'[age_chart] {time_id}'
    git.stage_commit_and_push(message)


def copy_css():
    css_file = os.path.join(DIR_GIT_GH_PAGES, 'styles.css')
    shutil.copyfile(CSS_FILE, css_file)


def render_head():
    return _('head', [
        _('link', None, dict(rel='stylesheet', href='styles.css'))
    ])


def render_mp(item):
    i, mp = item
    img_src = os.path.join(
        'https://raw.githubusercontent.com/nuuuwan/parliament_lk/data',
        f'mp_images/{mp.url_num}.jpg'
    )
    return _('tr', [
        _('td', [_('div', f'#{i + 1}', {'class': "div-row"})]),
        _('td', [_('img', None, dict(src=img_src))]),
        _('td', [_('div', mp.name_clean, {'class': "div-name"})]),
        _('td', [_('div', [
            _('div', mp.party_short, {'class': "div-party"}),
            _(
                'div',
                mp.electoral_district,
                {'class': "div-electoral-district"},
            ),
        ])]),
        _('td', [_('div', f'Age {mp.age}', {'class': "div-age"})]),
    ])


def render_mps():
    mps = sorted(MP.loadMPs(), key=lambda mp: -mp.age)

    return list(map(render_mp, enumerate(mps)))


def render_body():
    rendered_mps = render_mps()

    return _('body', [
        _('h1', 'Parliament of Sri Lanka'),
        _('table', [_('tbody', rendered_mps)]),
    ])


def render_html():
    html_file = os.path.join(DIR_GIT_GH_PAGES, 'index.html')
    html = _('html', [render_head(), render_body()])
    html.store(html_file)
    log.info(f'Saved {html_file}')


def main():
    git = git_download()
    copy_css()
    render_html()
    git_upload(git)


if __name__ == '__main__':
    main()
