import os
from dataclasses import dataclass
from functools import cached_property

from utils import JSONFile, Log

log = Log("Member")


@dataclass
class Member:
    mp_id: str
    district: str
    date_of_birth: str
    religion: str
    civil_status: str
    legislative_service: str
    profession: str
    address_sitting: str
    address_non_sitting: str
    phone_sitting: str
    phone_non_sitting: str
    email: str
    fax: str

    def to_dict(self):
        return {
            "mp_id": self.mp_id,
            "district": self.district,
            "date_of_birth": self.date_of_birth,
            "religion": self.religion,
            "civil_status": self.civil_status,
            "legislative_service": self.legislative_service,
            "profession": self.profession,
            "address_sitting": self.address_sitting,
            "address_non_sitting": self.address_non_sitting,
            "phone_sitting": self.phone_sitting,
            "phone_non_sitting": self.phone_non_sitting,
            "email": self.email,
            "fax": self.fax,
        }

    @classmethod
    def from_dict(Class, d):
        return Class(
            mp_id=d["mp_id"],
            district=d["district"],
            date_of_birth=d["date_of_birth"],
            religion=d["religion"],
            civil_status=d["civil_status"],
            legislative_service=d["legislative_service"],
            profession=d["profession"],
            address_sitting=d["address_sitting"],
            address_non_sitting=d["address_non_sitting"],
            phone_sitting=d["phone_sitting"],
            phone_non_sitting=d["phone_non_sitting"],
            email=d["email"],
            fax=d["fax"],
        )
