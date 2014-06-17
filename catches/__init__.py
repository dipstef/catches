from .catch_list import CatchList
from .handler import ErrorsHandler


class ErrorCatches(CatchList):

    def __init__(self, *catches):
        super(ErrorCatches, self).__init__((ErrorsHandler(errors, handler) for errors, handler in catches))

    def __setitem__(self, error_classes, handler):
        errors_handler = ErrorsHandler(error_classes, handler)
        self.add(errors_handler)

    def get(self, error_class):
        '''If the exception does not match a catch clause than check for parent classes'''
        return super(ErrorCatches, self).get(error_class) or self._resolve_from_base_errors(error_class)

    def handler(self, error_class):
        catch = self.get(error_class)
        if catch:
            return catch.handler

    def _resolve_from_base_errors(self, error):
        base_errors_catches = self._base_errors(error)
        if base_errors_catches:
            return super(ErrorCatches, self).get(base_errors_catches[0])


class ErrorCatchesAppend(ErrorCatches):

    def __init__(self, *catches):
        super(ErrorCatchesAppend, self).__init__()
        for errors, handler in catches:
            self.append(ErrorsHandler(errors, handler))

    def append(self, catch):
        self._append(catch)

    def remove_catch(self, *catches):
        removed = super(ErrorCatchesAppend, self).remove_catch(*catches)
        errors_removed = [error for catch in removed for error in catch.errors]
        self._map_errors_to_remaining_catches(errors_removed)
        return removed

    def _map_errors_to_remaining_catches(self, removed_errors):
        for catch in self._catches:
            for error in catch.errors:
                if error in removed_errors and not error in self._errors_catch:
                    self._errors_catch[error] = catch


class handle(object):
    def __init__(self, *errors):
        assert errors
        self._errors = errors

    def doing(self, handler):
        return ErrorsHandler(self._errors, handler)

catch = ErrorCatches
append = ErrorCatchesAppend