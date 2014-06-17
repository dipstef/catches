from collections import namedtuple
import inspect


class ErrorMatching(object):

    def matches(self, error):
        return any(self.matching(error))

    def _matching(self, error):
        return (error for error in base_errors(error) if error in self.errors)

    def matching(self, error):
        return list(self._matching(error))


class ErrorHandle(namedtuple('ErrorHandle', ['error', 'handler']), ErrorMatching):

    def __new__(cls, error, handler):
        assert issubclass(error, BaseException)
        return super(ErrorHandle, cls).__new__(cls, error, handler)

    @property
    def errors(self):
        return self.error,


class ErrorsHandler(namedtuple('ErrorHandlers', ['errors', 'handler']), ErrorMatching):

    def __new__(cls, errors, handler):
        if isinstance(errors, type):
            errors = (errors, )
        if len(errors) == 1:
            return ErrorHandle(errors[0], handler)
        else:
            assert all((issubclass(error_class, BaseException) for error_class in errors))
            return super(ErrorsHandler, cls).__new__(cls, tuple(errors), handler)


def base_errors(error_class):
    return (cls for cls in inspect.getmro(error_class) if issubclass(cls, BaseException))