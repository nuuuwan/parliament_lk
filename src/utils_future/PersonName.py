import re
from dataclasses import dataclass


@dataclass
class PersonName:

    names: list[str]

    @classmethod
    def from_str(Class, x):
        for k in [
            ", M.P.",
            ", M.P",
            ", MP",
            "(Alhaj)",
            "(Dr.)",
            "(Mrs.)",
            "(Ven.)",
            "Hon.",
            "Thero",
            "THERO",
        ]:
            x = x.replace(k, "")

        x = x.replace(".", " ")

        x = re.sub(r"\s+", " ", x)
        x = x.strip().title()

        lastname, _, firstnames = x.partition(",")
        names = firstnames.strip().split(" ") + lastname.strip().split(" ")
        names = [n for n in names if n]
        return PersonName(names)

    def to_dict(self):
        return {
            "names": self.names,
        }

    @classmethod
    def from_dict(Class, d):
        return Class(**d)
