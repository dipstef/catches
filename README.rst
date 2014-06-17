catches
=======

catches is a library that represents a try/except hierarchy, that can be modified dynamically.
Each error class maps to an handler.

Usage
-----
catches can invoke a function and handle errors differently.

.. code-block:: python

    from catches import handle, execute

    def raise_value(value):
        def raiser():
            raise ValueError(value)
        return raiser


    def no_foo(e):
        if e.message == 'foo':
            raise Exception('No Foo')
        return e.message
        
    >>> execute(raise_value('foo'), catch=(handle(ValueError).doing(no_foo)))
    Exception('No Foo!')

handlers can return values too:
.. code-block:: python

    >>> execute(raise_value('bar'), catch=(handle(ValueError).doing(no_foo)))
    'bar'
and base errors are handled:
.. code-block:: python
   >>> execute(raise_value('foo'), catch=(handle(StandardError).doing(no_foo)))
   Exception('No Foo!')
   >>> execute(raise_value('foo'), catch=(handle(Exception).doing(no_foo)))
   Exception('No Foo!')
