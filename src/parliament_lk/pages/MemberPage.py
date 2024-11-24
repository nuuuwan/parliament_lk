import os
from functools import cached_property

from utils import JSONFile, Log

from parliament_lk.core import Member
from utils_future import WebPage

log = Log("MemberPage")


class MemberPage(WebPage):
    def __init__(self, member_short_info):
        super().__init__(
            "https://beta.parliament.lk"
            + "/en/members-of-parliament/mp-profile"
            + f"/{member_short_info.mp_id}"
        )
        self.member_short_info = member_short_info

    @classmethod
    def get_dir_data(cls):
        return os.path.join(cls.get_temp_dir(), "data")

    @cached_property
    def json_path(self):
        dir_data = self.get_dir_data()
        os.makedirs(dir_data, exist_ok=True)
        return os.path.join(dir_data, f"{self.member_short_info.mp_id}.json")

    @cached_property
    def json_file(self):
        return JSONFile(self.json_path)

    @cached_property
    def member_nocache(self):

        div_data_list = self.soup.find_all("div", class_="text_tag")
        d = {}
        for div_data in div_data_list:
            p_list = div_data.find_all("p")
            k = p_list[0].text
            v = p_list[1].text
            d[k] = v

        return Member(
            mp_id=self.member_short_info.mp_id,
            name=self.member_short_info.name,
            district=d.get("District"),
            date_of_birth=d.get("Date of Birth"),
            religion=d.get("Religion"),
            civil_status=d.get("Civil Status"),
            legislative_service=d.get("Legislative Service"),
            profession=d.get("Profession"),
            address_sitting=d.get("Address (Sitting Days)"),
            address_non_sitting=d.get("Address (Non-Sitting Days)"),
            phone_sitting=d.get("Phone"),
            phone_non_sitting=d.get("Phone (Non-Sitting Days)"),
            email=d.get("Email"),
            fax=d.get("Fax"),
        )

    @cached_property
    def member(self):
        if self.json_file.exists:
            return Member.from_dict(self.json_file.read())
        member = self.member_nocache
        self.json_file.write(member.to_dict())
        log.debug(f"Wrote {self.json_path}")
        return member


if __name__ == "__main__":
    print(MemberPage(1247).member)
