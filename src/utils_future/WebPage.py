import os
import tempfile
from functools import cached_property

import requests
from bs4 import BeautifulSoup
from utils import File, Hash, Log

log = Log("WebPage")


class WebPage:

    @classmethod
    def get_temp_dir(cls):
        temp_dir = os.path.join(
            tempfile.gettempdir(), "parliament_lk", cls.__name__.lower()
        )
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    def __init__(self, url):
        self.url = url

    @cached_property
    def id(self):
        return Hash.md5(self.url)[:16]

    def __hash__(self):
        return hash(self.id)

    @cached_property
    def html_path(self):
        dir_html = os.path.join(self.get_temp_dir(), "html")
        os.makedirs(dir_html, exist_ok=True)
        return os.path.join(dir_html, f"{self.id}.html")

    @cached_property
    def html_file(self):
        return File(self.html_path)

    @cached_property
    def html(self):
        if not self.html_file.exists:
            log.debug(f"🌏 Downloading {self.url}")
            response = requests.get(self.url)
            html = response.text
            n_html = len(html)
            log.debug(f"Wrote {self.html_path} ({n_html:,}B)")
            self.html_file.write(html)
            return html
        return self.html_file.read()

    @cached_property
    def soup(self):
        return BeautifulSoup(self.html, "html.parser")
