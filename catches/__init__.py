from .catch_list import CatchList
from .handler import ErrorsHandler, Catch


class ErrorCatches(CatchList):

    def __init__(self, *catches):
        super(ErrorCatches, self).__init__((ErrorsHandler(errors, handler) for errors, handler in catches))

    def __setitem__(self, error_classes, handler):
        errors_handler = ErrorsHandler(error_classes, handler)
        self.add(errors_handler)

    def get(self, error_class):
        '''If the exception does not match a catch clause than check for parent classes'''
        error_catch = super(ErrorCatches, self).get(error_class)
        if not error_catch:
            return self._resolve_from_base_errors(error_class)
        return Catch(error_class, error_catch)

    def handler(self, error_class):
        catch = self.get(error_class)
        if catch:
            return catch.handler

    def _resolve_from_base_errors(self, error):
        base_errors_catches = self._base_errors(error)
        if base_errors_catches:
            base_catch = base_errors_catches[0]
            error_catch = super(ErrorCatches, self).get(base_catch)
            if error_catch:
                return Catch(base_catch, error_catch)


class ErrorCatchesConcatenation(ErrorCatches):

    def __init__(self, *catches):
        super(ErrorCatchesConcatenation, self).__init__()
        for errors, handler in catches:
            self.append(ErrorsHandler(errors, handler))

    def append(self, catch):
        self._append(catch)

    def remove(self, *catches):
        removed = super(ErrorCatchesConcatenation, self).remove(*catches)
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
concatenate = ErrorCatchesConcatenation


def execute(fun, catch=()):
    catches = concatenate(*catch)
    try:
        return fun()
    except catches.errors, e:
        error_handler = catches.handler(e.__class__)

        return error_handler(e)