Settings
========

`Kickoff` provides a way of fine tuning specific settings through ``kickoff.config`` data structure. It is recommended to do this in a code which is conditionally unavailable. For example:

.. code:: python

	if __name__ == "__kickoff__":
	    import kickoff
	    kickoff.config.prog_name = "demo"
	    kickoff.config.version_option = dict(version='1.2.3')
	    kickoff.config.help_option_names = ['-h', '--help']

This is how we can keep the module reusable in environments where `Kickoff` is not installed.

Available options can be found in the table below. Corresponding example: `ex05_customization <https://github.com/gergelyk/python-kickoff/blob/master/examples/ex05_customization/demo.py>`_.

======================= ========================================== ==============================================================================================================================================================
Option                  Default Value                              Description
======================= ========================================== ==============================================================================================================================================================
``accept_imported``     ``False``                                  Inspect entire content of given module, not only functions and classes defined locally.
``scan_recursively``    ``True``                                   Inspect classes (allows for creating command groups).
``black_list``          ``[]``                                     Functions and classes to be explicitely skipped in the inspection process.
``prog_name``           ``None``                                   Name of the application to be used in context help.
``prompt_caption``      ``None``                                   Text to be displayed at the beginngin of the prompt.
``prompt_suffix``       ``> ``                                     Text to be displayed at the end of the prompt.
``help_option_names``   ``None``                                   Dictionary to be unpacked to the arguments of `click.help_option <https://click.palletsprojects.com/en/7.x/api/#click.help_option>`__.
``version_option``      ``None``                                   Dictionary to be unpacked to the arguments of `click.version_option <https://click.palletsprojects.com/en/7.x/api/#click.version_option>`__ function.
``enable_repl``         ``True``                                   Makes ``--repl`` option available in top level CLI of your application.
``enable_gui``          ``True``                                   Makes ``--gui`` option available in top level CLI of your application (if only required dependencies are installed).
``enable_didyoumean``   ``True``                                   Provides the user with suggestions about misspelled commands.
``enable_history``      ``True``                                   Preserve history in REPL. History is stored in ``~/.{prog_name}_history`` file.
``command_wrapper``     ``kickoff.default_command_wrapper``        Function that wraps each of your commands.
``error_handler``       ``None``                                   Custom exception handler function.
======================= ========================================== ==============================================================================================================================================================







