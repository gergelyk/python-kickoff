Basic Concepts
==============

There is a very similar logic behind how Python3 handles arguments of the callables and how typical CLI handles arguments provided by the user. This fact makes `Kickoff` able to translate signatures of your functions into corresponding CLI commands. Table below summarizes this relationship.

============================================= ========================== ========================= ==========================
Function Argument                             Example                    Command Line Argument     Example
============================================= ========================== ========================= ==========================
None                                          ``foobar()``               None                      ``foobar``
Argument without default value                ``foobar(qux)``            Required parameter        ``foobar <QUX>``
Argument with default value                   ``foobar(qux=123)``        Optional parameter        ``foobar [<QUX>]``
Argument with default value of boolean type   ``foobar(*, qux=False)``   Flag                      ``foobar [--qux]``
Keyword-only argument without default value   ``foobar(*, qux)``         Required option           ``foobar --qux <QUX>``
Keyword-only argument with default value      ``foobar(*, qux=123)``     Optional option           ``foobar [--qux <QUX>]``
Non-keyworded variable-length argument list   ``foobar(*args)``          Optional multi-parameter  ``foobar [<ARGS> ...]``
Keyworded variable-length argument list       ``foobar(**kwargs)``       Ignored                   ``foobar``
============================================= ========================== ========================= ==========================

See `ex01_simple <https://github.com/gergelyk/python-kickoff/blob/master/examples/ex01_simple/demo.py>`_ to gain some experience.

You might have noticed that docstrings in the code can be used for providing descriptions. In addition, annotations can be used to specify details which cannot be distinguished from Python syntax. `Kickoff` expects annotations to be of ``dict`` type. Keys of the dictionary are passed to `click.argument <https://click.palletsprojects.com/en/7.x/api/?highlight=option#click.argument>`__ or `click.option <https://click.palletsprojects.com/en/7.x/api/?highlight=option#click.option>`__ function as corresponding parameters. Additionally ``alias`` can be used to specify short name of given CLI option. Values of return annotation are used as arguments to `click.Command <https://click.palletsprojects.com/en/7.x/api/#click.Command>`__ class.

Table below shows couple of practical examples on how to use annotations.

======================================================= ========================================================= ========================== ==============================
Function Argument                                       Example                                                   Command Line Argument      Example
======================================================= ========================================================= ========================== ==============================
``required`` specifier & variable-length argument list  ``foobar(*qux: dict(required=True))``                     Required multi-parameter   ``foobar <ARGS> ...``
``multiple`` specifier                                  ``foobar(*, qux: dict(multiple=True)``                    Required multi-option      ``foobar --qux <QUX> ...``
``multiple`` & ``required`` specifiers                  ``foobar(*, qux: dict(multiple=True, required=False))``   Optional multi-option      ``foobar [--qux <QUX> ...]``
``count`` specifier                                     ``foobar(*, qux: dict(count=True) )``                     Required counting flag     ``foobar --qux ...``
``count`` specifier & default value                     ``foobar(*, qux: dict(count=True) =0 )``                  Optional counting flag     ``foobar [--qux ...]``
======================================================= ========================================================= ========================== ==============================

Example `ex02_args_and_opts <https://github.com/gergelyk/python-kickoff/blob/master/examples/ex02_args_and_opts/demo.py>`_ covers more use cases. Note that settings specified in annotations overwite those which were deduced from function signature.

Please also check :ref:`Command Groups` chapter to see full mapping of Python AST elements and CLI elements.
