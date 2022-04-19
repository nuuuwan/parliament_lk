
from parliament_lk import scrape_mem

TEST_URL = 'https://www.parliament.lk' \
    + '/en/members-of-parliament'\
    + '/directory-of-members/viewMember/1234'

TEST_HTML_PARTY = '''
<tr>
    <td>
        <div>Party</div>
        <a>United National Party (UNP)</a>
    </td>
</tr>
'''

TEST_HTML_DATE_OF_BIRTH = '''
<tr><td>Date of Birth : 1234-05-06</td></tr>
'''

TEST_HTML_EMAIL = f'''
<tr>
    <td><img src="{scrape_mem.IMG_SRC_EMAIL}"/></td>
    <td>albert@einstein.org</td>
</tr>
'''

TEST_HTML_CONTACT = f'''
<tr>
    <table>
        <tr>
            <td>Non Sitting</td>
            <td>Sitting</td>
        </tr>
        <tr>
            <td>
                <table>
                    <tr>
                        <td><img src="{scrape_mem.IMG_SRC_PHONE}"/></td>
                        <td>0123456789</td>
                    </tr>
                    <tr>
                        <td><img src="{scrape_mem.IMG_SRC_ADDRESS}"/></td>
                        <td>Princeton, NJ</td>
                    </tr>
                </table>
            </td>
            <td>
                <table>
                    <tr>
                        <td><img src="{scrape_mem.IMG_SRC_PHONE}"/></td>
                        <td>0149779419</td>
                    </tr>
                    <tr>
                        <td><img src="{scrape_mem.IMG_SRC_ADDRESS}"/></td>
                        <td>
                            123 Home Street
                            </br>
                            Princeton, NJ
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</tr>
'''

TEST_HTML_DIV_CONTENT = f'''
<div class="components-wrapper">
    <h2>Albert Einstein</h2>
    {TEST_HTML_PARTY}
    <tr>
        <td>
            <div>Electoral District / National List</div>
            <a>Colombo</a>
        </td>
    </tr>

    {TEST_HTML_DATE_OF_BIRTH}
    <tr><td>Civil Status : Married</td></tr>
    <tr><td>Religion : Catholic</td></tr>
    <tr><td>Profession / Occupation : Physicist</td></tr>

    {TEST_HTML_CONTACT}
    {TEST_HTML_EMAIL}
</div>
'''

TEST_HTML = f'''
<html>
    {TEST_HTML_DIV_CONTENT}
</html>
'''
