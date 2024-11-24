import os
from functools import cached_property

from utils import JSONFile, Log, Parallel

from parliament_lk.core import MemberShortInfo
from utils_future import PersonName, WebPage

log = Log("MemberDirectoryPage")


class MemberDirectoryPage(WebPage):
    @classmethod
    def get_url(cls, prefix, limit, is_past):
        past_prefix = "past-" if is_past else ""
        url = (
            "https://beta.parliament.lk"
            + f"/en/members-of-parliament/{past_prefix}mp-listing"
            + f"?itemCount={limit}"
        )
        if prefix:
            url += f"&name={prefix}"

        return url

    def __init__(self, prefix, limit, is_past):
        super().__init__(self.get_url(prefix, limit, is_past))
        self.prefix = prefix
        self.limit = limit
        self.is_past = is_past

    @classmethod
    def get_dir_data(cls):
        return os.path.join(cls.get_temp_dir(), "data")

    @cached_property
    def json_path(self):
        dir_data = self.get_dir_data()
        os.makedirs(dir_data, exist_ok=True)
        return os.path.join(
            dir_data, f"{self.prefix}-{self.limit}-{self.is_past}.json"
        )

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

            div_name = div_member.find(
                "div",
                class_="pmp_name_div" if self.is_past else "mp_name_div",
            )
            p_name = div_name.find("p")
            raw_full_name = p_name.text.strip()
            name = PersonName.from_str(raw_full_name)

            mp_short_info = MemberShortInfo(mp_id=mp_id, name=name)

            member_short_info_list.append(mp_short_info)

        log.debug(f"Found {len(member_short_info_list)} members")
        return member_short_info_list

    @cached_property
    def member_short_info_list(self):
        if self.json_file.exists:
            d_list = self.json_file.read()
            return MemberShortInfo.list_from_d_list(d_list)

        member_short_info_list = self.member_short_info_list_nocache
        d_list = [m.to_dict() for m in member_short_info_list]
        self.json_file.write(d_list)
        log.debug(f"Wrote {self.json_path}")
        return member_short_info_list

    @classmethod
    def aggregate(Class):
        dir_data = Class.get_dir_data()
        all_member_short_info_list = []
        for f in os.listdir(dir_data):
            if not f.endswith(".json") and f != "all.json":
                continue
            path = os.path.join(dir_data, f)
            json_file = JSONFile(path)
            if not json_file.exists:
                continue

            d_list = json_file.read()
            member_short_info_list = MemberShortInfo.list_from_d_list(d_list)
            all_member_short_info_list.extend(member_short_info_list)

        # dedupe
        all_member_short_info_list = MemberShortInfo.dedupe(
            all_member_short_info_list
        )
        all_path = os.path.join(dir_data, "all.json")
        JSONFile(all_path).write(
            [m.to_dict() for m in all_member_short_info_list]
        )
        log.info(
            f"Wrote {len(all_member_short_info_list):,} members to {all_path}"
        )
        return all_member_short_info_list

    @classmethod
    def list_all(Class):
        workers = []
        for is_past in [True, False]:

            def worker(prefix=None, is_past=is_past):
                MemberDirectoryPage(
                    prefix=prefix, limit=2048, is_past=is_past
                ).member_short_info_list

            workers.append(worker)

        Parallel.run(workers)
        return MemberDirectoryPage.aggregate()


if __name__ == "__main__":
    MemberDirectoryPage.list_all()
