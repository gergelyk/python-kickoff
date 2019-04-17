Startup
=======

Invocation
----------

There are two options of specifying top-level module for `Kickoff` to execute.

* By providing name of the local module or system module.
* By providing absolute of relative path to your `.py` file. Thanks to this feature you can use `Kickoff` in the shebang: ``#!/usr/bin/env kickoff``.

Invoke ``kickoff`` without any parameters to get more explanations.


Initialization
--------------

Special ``kickoffcustomize.py`` file is loaded at the very beginning of `Kickoff` startup procedure. Crease this file in your `CWD <https://en.wikipedia.org/wiki/Working_directory>`__ if you need to perform any early configuration. Example can be found `here <https://github.com/gergelyk/python-kickoff/blob/master/examples/kickoffcustomize.py>`__.

Note that ``kickoffcustomize.py`` is expected to be used only during development. It is supposed to make live of developers easier, but it is not really expected to be delivered to the users. In production code you should rely on common Python practices, for example ``sitecustomize.py`` and ``usercustomize.py`` files.

