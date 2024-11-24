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
            ", PC",
            "(Alhaj)",
            "(Dr.)",
            "(Mr.)",
            "(Mrs.)",
            "(Ms. )",
            "(Prof.)",
            "(Ven.)",
            "Attorney at Law",
            "Hon.",
            "Mr.",
            "Mr",
            "Mrs",
            "Thero",
            "THERO",
            "Ven.",
            "Ven",
        ]:
            x = x.replace(k, "")

        x = x.replace(".", " ")

        x = re.sub(r"\s+", " ", x)
        x = x.strip().title()

        lastname, _, firstnames = x.partition(",")
        names = firstnames.replace(",", " ").strip().split(
            " "
        ) + lastname.strip().split(" ")
        names = [n for n in names if n]
        return PersonName(names)

    def to_dict(self):
        return " ".join(self.names)

    @classmethod
    def from_dict(Class, d):
        return Class(names=d.split(" "))
