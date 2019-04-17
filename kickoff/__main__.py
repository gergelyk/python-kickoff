import sys
import logging
from .loader import Loader
from .builder import CmdGroupsManager
from .helpers import load_customize_file, parse_args
from .exceptions import global_exception_guard
from .logger import log

def main():
    """An entry point of `kickoff` command"""

    with global_exception_guard():
        load_customize_file()

        resource_path, resource_name, app_args = parse_args(sys.argv)
        loader = Loader(resource_path, resource_name)
        config, commands, galaxy, app_name, app_doc = loader.get_resources()
        groups_mgr = CmdGroupsManager(galaxy, config, app_doc, app_name)

        for name, cmd in commands.items():
            groups_mgr.add_command(name, cmd)

        groups_mgr.run_top_group(app_args)


if __name__ == "__main__":
    main()
