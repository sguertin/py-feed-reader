import json
from typing import Any, Type
from pathlib import Path

from dataclasses_json import DataClassJsonMixin, LetterCase, config, global_config

from core.utilities.datetime import DateTime

DATACLASSES_JSON = "dataclasses_json"


def to_iso_format(dt: DateTime | Any) -> str:
    return dt.isoformat()


def encode_path(path: Path) -> str:
    return path.as_uri()


global_config.encoders[DateTime] = to_iso_format
global_config.decoders[DateTime] = DateTime.fromisoformat
global_config.encoders[Path] = encode_path
global_config.decoders[Path] = Path.from_uri


class CamelCaseJsonMixin(DataClassJsonMixin):
    dataclass_json_config: dict = config(letter_case=LetterCase.CAMEL)[DATACLASSES_JSON]

    @classmethod
    def list_to_json(
        cls: type[CamelCaseJsonMixin], iter: list[CamelCaseJsonMixin]
    ) -> str:
        return json.dumps([i.to_dict() for i in iter])

    @classmethod
    def json_to_list(cls: type[CamelCaseJsonMixin], json_string: str) -> list[Any]:
        return [cls.from_dict(i) for i in json.loads(json_string)]
