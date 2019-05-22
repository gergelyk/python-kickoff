Command Groups
==============

Developers of modern applications tend to arange commands of their CLI in groups. `Kickoff` looks at the code composition and reflects it in the hierarchical design of CLI. It recursively traverses across the module of your choice to find functions and classes. Functions become commands. Classes are interpreted as command groups.

By default only those functions which have their body defined in given module can become commands. This prevents form exposing of utility functions that the script may import from other modules for internal use. Also functions and classes names of which start with underscore are ignored.

Despite of this fact, it is possible to create a design which is divided into multiple files. To accept external code in the top level module, dedicated option must be set explicitly. This topic will be covered in :ref:`Distributed Design`. For now, here is an example of what we have discussed: `ex03_command_groups <https://github.com/gergelyk/python-kickoff/blob/master/examples/ex03_command_groups/demo.py>`_.

Following table explains the details on how `Kickoff` translates elements of Python AST into building blocks from `click` module.

============================================================ ================================
Python AST                                                   Click
============================================================ ================================
Function                                                     Command
Static method                                                Command
Class method                                                 Command
Function argument                                            Parameter or option
Class                                                        Command group
Return value annotation                                      Command settings
Argument annotation                                          Parameter/option settings
Function docstring                                           Command description
Class docstring                                              Command group description
Module docstring                                             Application description
============================================================ ================================

