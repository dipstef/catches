catches
=======

catches is a library that represents a try/except hierarchy, that can be modified dynamically.
Each error class maps to an handler.

Usage
-----
catches can invoke a function and handle errors differently. 

.. code-block:: python

    from catches import handle, execute
    def foo():
        raise Exception('No Foo')


    def bar():
        raise Exception('bar')


    def no_foo(e):
        if e.message == 'Foo':
            raise e
        return e.message

Invoking:
    >>> execute(foo, catch=(handle(Exception).doing(no_foo)))
Exception: No Foo!

Handler can return also results:
    >>> execute(bar, catch=(handle(Exception).doing(no_foo)))
'bar'
