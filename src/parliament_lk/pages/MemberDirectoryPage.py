import os
from functools import cached_property

from utils import JSONFile, Log

from parliament_lk.core import MemberShortInfo
from utils_future import PersonName, WebPage

log = Log("MemberDirectoryPage")


class MemberDirectoryPage(WebPage):
    @classmethod
    def get_url(cls, prefix, limit):
        return (
            "https://beta.parliament.lk"
            + "/en/members-of-parliament/past-mp-listing"
            + f"?name={prefix}&itemCount={limit}"
        )

    def __init__(self, prefix, limit):
        super().__init__(self.get_url(prefix, limit))
        self.prefix = prefix
        self.limit = limit

    @cached_property
    def json_path(self):
        dir_data = os.path.join(self.get_temp_dir(), "data")
        os.makedirs(dir_data, exist_ok=True)
        return os.path.join(dir_data, f"{self.prefix}-{self.limit}.json")

    @cached_property
    def json_file(self):
        return JSONFile(self.json_path)

    @cached_property
    def member_short_info_list_nocache(self):
        div_member_list = self.soup.find_all("div", class_="col-xxl-3")
        member_short_info_list = []
        for div_member in div_member_list:
            a = div_member.find("a")
            if not a or "members-of-parliament/mp-profile" not in a.get(
                "href"
            ):
                continue

            mp_id = a.get("href").split("/")[-1]

            div_name = div_member.find("div", class_="pmp_name_div")
            raw_full_name = div_name.text.strip()
            name = PersonName.from_str(raw_full_name)

            mp_short_info = MemberShortInfo(mp_id=mp_id, name=name)

            member_short_info_list.append(mp_short_info)
            print(
                mp_short_info,
            )

        log.debug(f"Found {len(member_short_info_list)} members")
        return member_short_info_list

    @cached_property
    def member_short_info_list(self):
        if self.json_file.exists:
            d_list = self.json_file.read()
            return [MemberShortInfo.from_dict(d) for d in d_list]

        member_short_info_list = self.member_short_info_list_nocache
        d_list = [m.to_dict() for m in member_short_info_list]
        self.json_file.write(d_list)
        log.debug(f"Wrote {self.json_path}")
        return member_short_info_list


if __name__ == "__main__":
    MemberDirectoryPage("A", 32).member_short_info_list
