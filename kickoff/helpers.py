from pathlib import Path
from .logger import log
from .exceptions import user_error_register, KickoffUsageError, UsagePrinter
from .loader import load_module

def load_customize_file():
    """Load kickoffcustomize.py from CWD or os.path"""

    try:
        load_module('kickoffcustomize')
    except ModuleNotFoundError as exc:
        if user_error_register.is_set(exc):
            raise
        else:
            log.debug(f"kickoffcustomize.py not found")


def parse_args(argv):
    UsagePrinter.exe_name = Path(argv[0]).name

    try:
        kickoff_arg = argv[1]
    except:
        raise KickoffUsageError("Startup module of script must be specified")

    app_args = argv[2:]

    sep = ':'
    parts = kickoff_arg.split(sep)
    field1 = sep.join(parts[:-1])
    field2 = parts[-1]

    if len(parts) == 1:
        path = field2
        name = None
    else:
        path = field1
        name = field2

    if not name:
        name = None

    if not path:
        path = None

    log.debug(f"Resource name: {name!r}")
    log.debug(f"Resource path: {path!r}")

    return path, name, app_args

