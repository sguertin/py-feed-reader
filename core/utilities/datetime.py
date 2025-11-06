from datetime import datetime, UTC, timezone
from typing_extensions import Self

TZ_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
OFFSET_FORMAT = "%a, %d %b %Y %H:%M:%S %z"

UTC: timezone = UTC


class DateTime(datetime):
    @classmethod
    def now(cls) -> Self:
        return super().now()

    @classmethod
    def utcnow(cls) -> Self:
        return super().now(UTC)

    @classmethod
    def utcnow_timestamp(cls) -> str:
        return super().now(UTC).strftime(TZ_FORMAT)

    @classmethod
    def strptime(cls, date_string: str, format: str) -> Self:
        return super().strptime(date_string, format)

    @classmethod
    def parse_timestamp(cls, date_string) -> Self:
        try:
            return super().strptime(date_string, OFFSET_FORMAT)
        except ValueError:
            pass
        try:
            return super().strptime(date_string, TZ_FORMAT)
        except ValueError:
            pass
        try:
            return super().fromisoformat(date_string)
        except ValueError:
            raise

    def timestamp(self) -> str:
        return self.strftime(TZ_FORMAT)

    def __str__(self) -> str:
        return self.isoformat()

    def __repr__(self) -> str:
        return f"DateTime(year={self.year},month={self.month},day={self.day}, hour={self.hour}, minute={self.minute}, second={self.second})"
