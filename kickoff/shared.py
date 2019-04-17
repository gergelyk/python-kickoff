import sys
import box

def get_config():
    """This provides the same config that is used in the user module"""
    try:
        return sys.modules['kickoff'].config
    except KeyError:
        # kickoff module doesn't seem to be imported in the user module
        return config


def default_command_wrapper(cmd, args, kwargs):
    ret = cmd(*args, **kwargs)
    if ret is not None:
        print(ret, file=sys.stderr)


def silent_command_wrapper(cmd, args, kwargs):
    ret = cmd(*args, **kwargs)


config = box.Box(accept_imported=False,
                 scan_recursively=True,
                 black_list=[],
                 error_handler=None,
                 command_wrapper=default_command_wrapper,
                 prog_name=None,
                 help_option_names=None,
                 version_option=None,
                 enable_repl=True,
                 enable_gui=True,
                 enable_didyoumean=True,
                 )
