Distributed Design
==================

In case of a complex application you may want to divide it into sub-modules. Good news is that general concepts of Python are applicable here. Two remarks need to be placed though:

* In order to let `Kickoff` know how to group commands imported from other modules, we need to import them in scopes of corresponding classes.

* `Kickoff` must be told explicitly to take external symbols into use. Otherwise they will be considered as utility functions that should not be exposed in CLI. This can be achieved by using ``kickoff.config.accept_imported`` setting. Settings will be covered in more details in :ref:`Settings` chapter. It also mentiones ``kickoff.config.black_list`` setting which can be used to have selected symbols skipped in analysis despite of their name and origin.

Let's don't spend more time on theoretical considerations. Example `ex04_distributed_design <https://github.com/gergelyk/python-kickoff/tree/master/examples/ex04_distributed_design>`_ is self-explanatory.

Note the example is designed to user ``demo.py`` as top level module. However it is also possible to invoke `Kickoff` against submodules for debugging purposes. Try the following:

.. code:: bash

    kickoff examples/ex04_distributed_design/demo.py
    kickoff examples/ex04_distributed_design/calc.py

