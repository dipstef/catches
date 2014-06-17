from catches import catch, handle, append
from tests import _one, _raise


def _remove_catches_test():
    catches = catch(handle(UnicodeDecodeError, UnicodeEncodeError).doing(_one))

    errors = catches.copy()

    assert errors.handler(UnicodeDecodeError) == _one

    assert errors.remove_error(UnicodeDecodeError) == (handle(UnicodeDecodeError).doing(_one), )
    assert errors.get(UnicodeEncodeError) == handle(UnicodeEncodeError).doing(_one)

    errors = catches.copy()
    errors.remove_catch(handle(UnicodeDecodeError).doing(_one))
    assert errors.handler(UnicodeEncodeError) == _one


def _remove_concatened_catches_test():
    catches = append(handle(UnicodeDecodeError, UnicodeEncodeError).doing(_one),
                     handle(UnicodeDecodeError).doing(_raise))

    errors = catches.copy()

    assert errors.handler(UnicodeDecodeError) == _one

    assert errors.remove_error(UnicodeDecodeError) == (handle(UnicodeDecodeError).doing(_one),
                                                       handle(UnicodeDecodeError).doing(_raise))
    assert errors.get(UnicodeEncodeError) == handle(UnicodeEncodeError).doing(_one)

    errors = catches.copy()
    errors.remove_catch(handle(UnicodeDecodeError, UnicodeEncodeError).doing(_one))
    assert errors.handler(UnicodeDecodeError) == _raise

    errors = catches.copy()
    errors.remove_catch(handle(UnicodeDecodeError).doing(_one))
    assert errors.handler(UnicodeEncodeError) == _one
    assert errors.handler(UnicodeDecodeError) == _raise


def main():
    _remove_catches_test()
    _remove_concatened_catches_test()

if __name__ == '__main__':
    main()