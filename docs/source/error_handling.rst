Error Handling
==============

In this chapter we will discuss what happens when exceptions are raised in functions used as CLI commands, or in descendent callables. In general `Kickoff` doesn't enforce any particular error handling strategy. It gives the developer freedom of implementing it according to his own preferences. On the other hand, `Kickoff` provides a set of helpers that can be utilized in this implementation. Before we elaborate on this topic, it is important to explain that application based on `Kickoff` consists of following layers:

.. code:: raw

    command function -> command wrapper -> click module -> kickoff module -> Python environment

This also reflects the path which an exception is going through from `command function` until it is finally catched.

Standard Exceptions
-------------------

Python build-in exceptions raised from `command function` by default reach Python environment and are handled by function registered in ``sys.excepthook``. Typically this prints call stack and error message to `stderr`. This is the same behavior as you would get by calling Python interpreter directly instead of invoking ``kickoff`` command.

Default `excepthook` can be replaced by user-defined hook using Python-provided `API <https://docs.python.org/3/library/sys.html#sys.excepthook>`_. However one may consider this more suitable to handle exceptions one step earlier, on the application level. For this purpose `Kickoff` provides own exception handler. It is recommended to use one of these exception handlers before providing the application to production. One of the proposed solutions is known as ``kickoff.simple_error_handler`` and comes together with ``kickoff`` package. It is implemented as follows:

.. code:: python

    def simple_error_handler(exc, *, file=sys.stderr, exit_code=EXIT_CODES.USAGE_USER):
        print(f"Error: {exc}", file=file)
        if hasattr(exc, 'exit_code'):
            exit_code = exc.exit_code
        exit(exit_code)

Once activated through ``kickoff.config.error_handler`` it hides call stack from the eyes of the user and provides him only with the error message. Application exits with error code `4`.

It is possible to disable exception handler registered in ``kickoff.simple_error_handler`` by setting environment variable ``KICKOFF_DEBUG`` to non-zero. In such case exceptions are handled by Python environment as normally during development.

Application-defined Exceptions
------------------------------

Exceptions specified by the developer are handled the same way as Python build-in exceptions. Additionally they can change default exit code returned by the application if they specify ``exit_code`` field in the exception class.

Kickoff Errors
--------------

Errors caused by incorrect usage of `Kickoff` module make the application exit with exit code equal `3`. For instance this is what happens when you invoke ``kickoff`` command without any arguments. This kind of exceptions are handled on `kickoff` module level and they are not propagated any further unless ``KICKOFF_DEBUG`` is set to non-zero.


Click Errors
------------

Errors caused by incorrect usage of CLI are handled by `click` module. This kind of errors can be raised by `click` module itself or by `command function`. Depending on their class, they may or may not result in having context help displayed. For example compare raising ``click.UsageError`` and ``click.BadOptionUsage``. `Click` errors cause the application exit with exit code equal `2`. This kind of exceptions are handled on `click` module level and they are not propagated any further.

It may be desired to derive application-defined exceptions from `click` exceptions as their occurrence doesn't terminate REPL.

.. note:: Command wrapper introduced in :ref:`Command Wrapper` chapter can be used to implement additional error handling.

.. note:: ``click_repl.ExitReplException`` can be raised to close REPL gently.

.. note:: Exceptions raised from ``kickoffcustomize`` described in :ref:`Startup` chapter are not handled by the function registered in ``kickoff.config.error_handler`` and go directly to Python environment.


Play with `ex07_error_handling <https://github.com/gergelyk/python-kickoff/blob/master/examples/ex07_error_handling/demo.py>`_ to see how different types of errors are handled.


