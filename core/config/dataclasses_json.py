from typing import Type
from dataclasses_json import DataClassJsonMixin, LetterCase, config


def camel_case(cls: Type[DataClassJsonMixin]) -> Type[DataClassJsonMixin]:
    cls.dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]
    return cls


class CamelCaseJsonMixin(DataClassJsonMixin):
    dataclass_json_config: dict = config(letter_case=LetterCase.CAMEL)[
        "dataclasses_json"
    ]
