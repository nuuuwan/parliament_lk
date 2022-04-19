
import unittest
from unittest.mock import MagicMock

from bs4 import BeautifulSoup
from utils import www

from parliament_lk import scrape_mem_dir

TEST_LI = '''
<li id="Albert Einstein">
    <a href="member/1234">Test</a>
</li>
'''

TEST_HTML = f'''
<html>
    <body>
        <div id="listholder">
            <ul>
                {TEST_LI}
            </ul>
        </div>
    </body>
</html>
'''


class TestCase(unittest.TestCase):
    def setUp(self):
        www.read = MagicMock(return_value=TEST_HTML)

    def test_get_url(self):
        self.assertEqual(
            'https://www.parliament.lk' +
            '/en/members-of-parliament/directory-of-members/?cletter=A',
            scrape_mem_dir.get_url('A'))

    def test_scrape_html(self):
        html = scrape_mem_dir.scrape_html('A')
        self.assertEqual(len(TEST_HTML), len(html))

    def test_parse_info(self):
        li = BeautifulSoup(TEST_LI, 'html.parser')
        info = scrape_mem_dir.parse_li(li)
        self.assertTrue(
            dict(name="Albert Einstein", url_num=1234),
            info,
        )

    def test_parse_html(self):
        mem_dir_info_list = scrape_mem_dir.parse_html(TEST_HTML)
        self.assertEqual(len(mem_dir_info_list), 1)

    def test_scrape_all_mem_dir(self):
        mem_dir_info_list = scrape_mem_dir.scrape_all()
        self.assertEqual(len(mem_dir_info_list), 26)


if __name__ == '__main__':
    unittest.main()
