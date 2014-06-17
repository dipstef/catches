from catches import handle, catch
from tests import _raise, _nothing, _one


def _extend_declarations_test():
    catches = catch(handle(ValueError, TypeError).doing(_one), handle(BaseException).doing(_raise))

    assert catches.handler(ValueError) == _one
    assert catches.handler(TypeError) == _one
    assert catches.handler(BaseException) == _raise
    assert catches.handler(StandardError) == _raise

    catches[(NotImplementedError, StandardError)] = _one
    catches[Exception] = _raise

    assert catches.catches == (((ValueError, TypeError), _one), ((NotImplementedError, StandardError), _one),
                              (Exception, _raise), (BaseException, _raise))

    assert catches.errors == (ValueError, TypeError, NotImplementedError, StandardError, Exception, BaseException)

    assert catches.handler(NotImplementedError) == _one
    assert catches.handler(StandardError) == _one
    assert catches.handler(Exception) == _raise
    #ValueError
    assert catches.handler(UnicodeDecodeError) == _one


def _add_intersecting_catches_test():
    catches = catch(handle(ValueError, TypeError).doing(_one), handle(BaseException).doing(_raise))

    catches[(ValueError, Exception)] = _one

    assert catches.catches == (((ValueError, TypeError), _one), (Exception, _one), (BaseException, _raise))


def _update_declarations_test():
    catches = catch(handle(ValueError, TypeError).doing(_one), handle(BaseException).doing(_raise))

    assert catches.handler(ValueError) == _one

    catches.add(handle(ValueError).doing(_nothing))
    assert catches.catches == ((ValueError, _nothing), (TypeError, _one), (BaseException, _raise))

    assert catches.handler(ValueError) == _nothing
    assert catches.handler(StandardError) == _raise

    catches.add(handle(StandardError).doing(_nothing))
    assert catches.catches == ((ValueError, _nothing), (TypeError, _one), (StandardError, _nothing),
                               (BaseException, _raise))

    assert catches.handler(StandardError) == _nothing


def _override_declarations_test():
    errors = catch(((ValueError, TypeError), _one), (BaseException, _raise))

    assert errors.handler(ValueError) == _one

    errors2 = errors.copy_with(handle(ValueError).doing(_nothing))
    assert errors2.catches == ((ValueError, _nothing), (TypeError, _one), (BaseException, _raise))

    assert errors2.handler(ValueError) == _nothing
    assert errors2.handler(StandardError) == _raise

    errors2 = errors.copy_with(handle(StandardError).doing(_nothing))
    assert errors2.catches == (((ValueError, TypeError), _one), (StandardError, _nothing), (BaseException, _raise))

    assert errors2.handler(StandardError) == _nothing


def _move_up_catch_test():
    catches = catch(handle(UnicodeDecodeError, UnicodeEncodeError).doing(_one))

    errors = catches.copy()
    errors.add(handle(ValueError).doing(_raise))

    assert errors.catches == (((UnicodeDecodeError, UnicodeEncodeError), _one), (ValueError, _raise))

    errors = catches.copy()

    errors.top(handle(ValueError).doing(_raise))

    assert errors.catches == ((ValueError, _raise), ((UnicodeDecodeError, UnicodeEncodeError), _one))

    errors = catches.copy()
    errors.top(handle(UnicodeDecodeError).doing(_raise))

    assert errors.catches == ((UnicodeDecodeError, _raise), (UnicodeEncodeError, _one))


def main():
    _extend_declarations_test()
    _add_intersecting_catches_test()
    _update_declarations_test()
    _override_declarations_test()
    _move_up_catch_test()

if __name__ == '__main__':
    main()