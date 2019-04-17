Command Wrapper
===============

`Kickoff` has been designed to be handy as a prototyping tool and at the same time to be suitable for production code. It allows you to test utility functions that are not supposed to became commands in the final code. For instance this is how you can examine ``findall`` function right from ``re`` module:

.. code:: bash

    $ kickoff :re findall "b\w*d" "beer bear bird bore beard"
    ['bird', 'beard']

In such case you are interested in the value returned by the targeted function. Moreover, functions exposed as CLI commands may also return values that can be used later for debugging purposes. For these reasons `Kickoff` wraps each of your functions in a default wrapper which prints returned value to `stderr`, unless returned value is ``None``:

.. code:: python

    def default_command_wrapper(cmd, args, kwargs):
        ret = cmd(*args, **kwargs)
        if ret is not None:
            print(ret, file=sys.stderr)

If you need to disable this behaviour, you can switch ``kickoff.config.command_wrapper`` to ``kickoff.silent_command_wrapper``. Alternatively you can define your own custom wrapper function which may implement additional functionality like verbose logging. Consider `ex06_command_wrapper <https://github.com/gergelyk/python-kickoff/blob/master/examples/ex06_command_wrapper/demo.py>`_.

Note that custom wrapper function can also catch and raise exceptions according to your error handling strategy. More about this topic in :ref:`Error Handling`.
