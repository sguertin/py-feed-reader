
from core.interfaces.common import ISave


def autosave(method):
    def wrapper(self: ISave, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.save()
        return result

    return wrapper
