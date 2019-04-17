import sys
import runpy
import inspect
import importlib
from pathlib import Path
from .logger import log
from .shared import get_config
from . import cmdpath
from . inspectutils import getfile, isstaticmethod
from .exceptions import user_exception_guard, KickoffUsageError, user_error_register

RUN_NAME = '__kickoff__'


def load_module(name, path=None):
    """ Load module into memory and add it to sys.path
    """
    log.debug(f"Loading module {name!r} from: {path}")

    if path:
        path_abs = str(Path(path).expanduser().absolute())
        sys.path.insert(0, path_abs)
        path_list = [path]
    else:
        path_list = None

    for finder in sys.meta_path:
        if hasattr(finder, 'find_spec'):
            spec = finder.find_spec(name, path_list)
            if spec is not None:
                break
    else:
        msg = f"No module named {name!r}"
        raise ModuleNotFoundError(msg, name=name)
    user_module = importlib.util.module_from_spec(spec)
    with user_exception_guard():
        spec.loader.exec_module(user_module)
    sys.modules[name] = user_module
    return user_module


def load_script(path):
    """ Run Python script script. Directory of the script will be added to sys.path
    """
    log.debug(f"Running script: {path}")
    script_dir = str(Path(path).expanduser().absolute().parent)
    sys.path.insert(0, script_dir)

    try:
        with open(path): pass
    except:
        raise KickoffUsageError(f"Script not accessible: {path}")

    with user_exception_guard():
        user_globals = runpy.run_path(path, run_name=RUN_NAME)

    return user_globals


class Loader:

    def __init__(self, resource_path, resource_name):
        self._galaxy = {}
        self._commands = {}

        self._load_resources(resource_name, resource_path)
        self._config = get_config()
        self._set_filters()
        self._scan_namespace(self._top_namespace, self._config.scan_recursively)


    def _load_resources(self, resource_name, resource_path):
        if resource_name:
            try:
                src_module = load_module(name=resource_name, path=resource_path)
            except ModuleNotFoundError as exc:
                if user_error_register.is_set(exc):
                    raise
                else:
                    raise KickoffUsageError(f"Module not accessible: {resource_name}") from exc

            top_namespace = vars(src_module)
            self._app_name = resource_name
            is_src_local = lambda item: inspect.getmodule(item[1]) is src_module
        else:
            top_namespace = load_script(path=resource_path)
            self._app_name = Path(resource_path).name
            def is_src_local(item):
                obj = item[1]
                if inspect.isclass(obj) and hasattr(obj, '__module__'):
                    return obj.__module__ is RUN_NAME
                else:
                    return getfile(obj) is resource_path

        self._is_src_local = is_src_local
        self._top_namespace = top_namespace


    def _set_filters(self):
        is_black = lambda c: c[1] in self._config.black_list
        is_function = lambda c: inspect.isfunction(c[1]) or isstaticmethod(c[1])
        is_public = lambda c: not c[0].startswith('_')
        is_class = lambda c: inspect.isclass(c[1])

        cls_filter = lambda c: is_public(c) and is_class(c) and not is_black(c)
        func_filter = lambda c: is_public(c) and is_function(c) and not is_black(c)

        if self._config.accept_imported:
            log.debug(f"Accepting imported")
            self.cls_filter = cls_filter
            self.func_filter = func_filter
        else:
            log.debug(f"Discarding imported")
            self.cls_filter = lambda c: cls_filter(c) and self._is_src_local(c)
            self.func_filter = lambda c: func_filter(c) and self._is_src_local(c)


    def _scan_namespace(self, namespace, recursively=False, path=cmdpath.root):
        """ takes:
                namespace - dictionary of variables to Scanning
                recursively - whether or not to dig into classes recursively
                path - tuple of strings that describes how to get to the namespace
            updates:
                self._galaxy - {namespace_path: namespace}
                self._commands - {function_name: function}
        """
        log.debug(f"Scanning namespace {path!r}")

        def extract_func(cmd):
            if isstaticmethod(cmd):
                return cmd.__func__
            else:
                return cmd

        commands_ = dict(filter(self.func_filter, namespace.items()))
        commands = {path / k: extract_func(v) for k, v in commands_.items() }
        self._galaxy[path] = namespace
        self._commands.update(commands)

        for cmd_name, cmd in commands.items():
            log.debug(f"Command {cmd.__qualname__!r} discovered under name {cmd_name!r}")

        if recursively:
            cls_dict = dict(filter(self.cls_filter, namespace.items()))

            for cls_name, cls in cls_dict.items():
                self._scan_namespace(vars(cls), recursively, path / cls_name)


    def get_resources(self):
        app_doc = self._top_namespace['__doc__']
        return self._config, self._commands, self._galaxy, self._app_name, app_doc



