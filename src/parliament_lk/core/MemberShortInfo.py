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
