from datetime import datetime, UTC

def utc_timestamp()->str:
    return datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')