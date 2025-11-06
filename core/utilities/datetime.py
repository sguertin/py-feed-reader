from datetime import datetime, UTC, timezone

TZ_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
OFFSET_FORMAT = "%a, %d %b %Y %H:%M:%S %z"

UTC: timezone = UTC


def utcnow_timestamp() -> str:
    return datetime.now(UTC).strftime(TZ_FORMAT)


def parse_timestamp(date_string: str) -> datetime:
    try:
        return datetime.strptime(date_string, OFFSET_FORMAT)
    except ValueError:
        pass
    try:
        return datetime.strptime(date_string, TZ_FORMAT)
    except ValueError:
        pass
    try:
        return datetime.fromisoformat(date_string)
    except ValueError:
        raise


class DateTime(datetime):
    @classmethod
    def now(cls) -> DateTime:
        return super().now()

    @classmethod
    def utcnow(cls) -> DateTime:
        return super().now(UTC)

    @classmethod
    def utcnow_timestamp(cls) -> str:
        return super().now(UTC).strftime(TZ_FORMAT)

    @classmethod
    def parse_timestamp(cls, date_string):
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

    def __str__(self):
        return self.isoformat()

    def __repr__(self) -> str:
        return f"DateTime(year={self.year},month={self.month},day={self.day}, hour={self.hour}, minute={self.minute}, second={self.second})"
