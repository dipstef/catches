Catches
=======

catches is a library that handles dynamically errors.

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

and errors are matched to their parent classes:

.. code-block:: python

   >>> execute(raise_value('foo'), catch=(handle(StandardError).doing(no_foo)))
   Exception('No Foo!')
   >>> execute(raise_value('foo'), catch=(handle(Exception).doing(no_foo)))
   Exception('No Foo!')

Error handlers are tuples:

.. code-block:: python

    from catches.handler import ErrorsHandler, ErrorHandler

    handler = handle(TypeError, ValueError).doing(no_foo)
    assert handler == ((TypeError, ValueError), no_foo) == ErrorsHandler((TypeError, ValueError), no_foo)

    handler = handle(TypeError).doing(no_foo)
    assert handler == (TypeError, no_foo) == ErrorsHandler((TypeError, ), no_foo) \
                   == ErrorHandler(TypeError, no_foo)

Handlers are overridden by highest member in the error class hierarchy

.. code-block:: python

   from catches import catch

   def bar_raiser(e):
        if e.message == 'bar':
            raise Exception('They took the whole bar!')
        return e.message

   errors = catch(handle(StandardError).doing(bar_raiser), handle(ValueError).doing(no_foo))

   assert errors.catches == ((ValueError, no_foo), (StandardError, bar_raiser))

   >>> execute(raise_value('bar'), catch=errors.catches)
   'bar'

   errors.uncatch(ValueError)
   assert errors.catches == ((StandardError, bar_raiser), )

   >>> execute(raise_value('bar'), catch=errors.catches)
   Exception('They took the whole bar!')

Base classes to existing catch blocks can be moved right on top:

.. code-block:: python

    errors.top(handle(Exception).doing(no_foo))
    assert errors.catches == ((Exception, no_foo), (StandardError, bar_raiser))
