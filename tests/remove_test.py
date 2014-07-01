from catches import catch, handle, concatenate
from tests import _one, _raise


def _remove_catches_test():
    catches = catch(handle(UnicodeDecodeError, UnicodeEncodeError).doing(_one))

    errors = catches.copy()

    assert errors.handler(UnicodeDecodeError) == _one

    assert errors.uncatch(UnicodeDecodeError) == (handle(UnicodeDecodeError).doing(_one), )
    assert handle(UnicodeEncodeError).doing(_one)

    errors = catches.copy()
    errors.remove(handle(UnicodeDecodeError).doing(_one))
    assert errors.handler(UnicodeEncodeError) == _one


def _remove_concateneted_catches_test():
    catches = concatenate(handle(UnicodeDecodeError, UnicodeEncodeError).doing(_one),
                          handle(UnicodeDecodeError).doing(_raise))

    errors = catches.copy()

    assert errors.handler(UnicodeDecodeError) == _one

    assert errors.uncatch(UnicodeDecodeError) == (handle(UnicodeDecodeError).doing(_one),
                                                  handle(UnicodeDecodeError).doing(_raise))
    assert errors.get(UnicodeEncodeError) == handle(UnicodeEncodeError).doing(_one)

    errors = catches.copy()
    errors.remove(handle(UnicodeDecodeError, UnicodeEncodeError).doing(_one))
    assert errors.handler(UnicodeDecodeError) == _raise

    errors = catches.copy()
    errors.remove(handle(UnicodeDecodeError).doing(_one))
    assert errors.handler(UnicodeEncodeError) == _one
    assert errors.handler(UnicodeDecodeError) == _raise


def main():
    _remove_catches_test()
    _remove_concateneted_catches_test()

if __name__ == '__main__':
    main()