from dataclasses import dataclass

from utils import Log

from utils_future import PersonName

log = Log("MemberShortInfo")


@dataclass
class MemberShortInfo:
    mp_id: str
    name: PersonName

    def to_dict(self):
        return {
            "mp_id": self.mp_id,
            "name": self.name.to_dict(),
        }

    @classmethod
    def from_dict(Class, d):
        return Class(
            mp_id=d["mp_id"],
            name=PersonName.from_dict(d["name"]),
        )

    @classmethod
    def list_from_d_list(Class, d_list):
        return [Class.from_dict(d) for d in d_list]

    @classmethod
    def dedupe(Class, member_short_info_list):
        idx = {}
        for m in member_short_info_list:
            idx[m.mp_id] = m

        arr = list(idx.values())
        arr.sort(key=lambda m: m.mp_id)
        return arr
