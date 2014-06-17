from catches import handle
from catches.handler import ErrorsHandler
from tests import _raise, _nothing


def _errors_handler_test():
    assert ErrorsHandler((ValueError, BaseException), _raise) == ((ValueError, BaseException), _raise)
    assert ErrorsHandler((ValueError, ), _raise) == (ValueError, _raise)

    assert handle(ValueError, BaseException).doing(_raise) == ((ValueError, BaseException), _raise)
    assert handle(ValueError).doing(_raise) == (ValueError, _raise)
    assert handle(Exception).doing(_nothing) == (Exception, _nothing)


if __name__ == '__main__':
    _errors_handler_test()