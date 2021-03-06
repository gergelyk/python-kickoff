import click
import inspect
import click_repl
from enum import IntEnum
from functools import wraps, partial
from pathlib import Path
from click_didyoumean import DYMGroup
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from .logger import log
from .exceptions import user_exception_guard
from .helpers import doc_to_short_help
from .inspectutils import get_all_defaults, unwrap, extract_func, isclassmethod
from .types import IntEnumParamType
from . import cmdpath


class KickoffCompleter(click_repl.ClickCompleter):
    def __init__(self, group, backlist):
        super().__init__(group)
        self._backlist = backlist

    def get_completions(self, document, complete_event=None):
        items = super().get_completions(document, complete_event)
        yield from [item for item in items if item.text not in self._backlist]


class CmdGroupsManager:
    """ Manage collection of command groups
    """

    def __init__(self, galaxy, config, app_doc, app_name):
        self._galaxy = galaxy
        self._config = config
        self._prog_name = self._config.prog_name or app_name
        self._prompt_caption =  self._config.prompt_caption or self._prog_name
        self._prompt_suffix = self._config.prompt_suffix
        top_group = self._create_top_group(app_doc)
        self._groups = {cmdpath.root: top_group}


    def _get_group_class(self):
        if self._config.enable_didyoumean:
            return DYMGroup
        else:
            return click.Group


    def _register_repl(self, target, cmd_name, blacklist):
        compl_blacklist = [f"--{cmd}" for cmd in blacklist]

        def repl_callback(ctx, param, value):
            if not value or ctx.resilient_parsing:
                return

            prompt_kwargs = {'completer': KickoffCompleter(ctx.command, compl_blacklist),
                             # simple text can be provided here if colors are not desired
                             'message': [('class:appname', self._prompt_caption),
                                         ('class:suffix',  self._prompt_suffix)],
                             'style': Style.from_dict({'appname': 'ansicyan bold',
                                                       'suffix':  'ansigray'}),
                             'enable_system_prompt': True,
                             'enable_open_in_editor': True, # CTRL+X CTRL+E
                             'complete_while_typing': True,
                             'auto_suggest': AutoSuggestFromHistory(),

                             # this works by default, if enabled explicitely complete_while_typing becomes disabled
                             #'enable_history_search': True, # CTRL+R
                            }

            if self._config.enable_history:
                prompt_kwargs['history'] = FileHistory(Path('~').expanduser() / f'.{self._prog_name}_history')

            click_repl.repl(ctx,
                            prompt_kwargs=prompt_kwargs,
                            allow_system_commands=True,
                            allow_internal_commands=False)
            ctx.exit()

        target = click.option(f'--{cmd_name}',
                              is_flag=True, expose_value=False, is_eager=False,
                              callback=repl_callback,
                              help="Start an interactive shell.")(target)
        return target


    def _register_gui(self, target, cmd_name, blacklist):

        try:
            import quick
        except ModuleNotFoundError as exc:
            log.debug(f"{exc}, GUI will not be available")
            return target

        def gui_callback(ctx, param, value):
            if not value or ctx.resilient_parsing:
                return
            ctx.command.params = [p for p in ctx.command.params if p.name not in blacklist]
            quick.gui_it(ctx.command)
            ctx.exit()

        target = click.option(f'--{cmd_name}',
                              is_flag=True, expose_value=False, is_eager=False,
                              callback=gui_callback,
                              help="Start GUI (experimental).")(target)
        return target


    def _create_top_group(self, doc):
        def target(): pass
        target.__doc__ = doc
        target.__name__ = self._prog_name # attribute inspected by quick module
        context_settings = {}

        if self._config.help_option_names is not None:
            context_settings['help_option_names'] = self._config.help_option_names

        blacklist = []
        repl_cmd_name = 'repl'
        gui_cmd_name = 'gui'

        if self._config.enable_repl:
            blacklist.append(repl_cmd_name)

        if self._config.enable_gui:
            blacklist.append(gui_cmd_name)

        if self._config.enable_repl:
            target = self._register_repl(target, repl_cmd_name, blacklist)

        if self._config.enable_gui:
            target = self._register_gui(target, gui_cmd_name, blacklist)

        group = click.group(cls=self._get_group_class(), context_settings=context_settings)(target)

        if self._config.version_option is not None:
            group = click.version_option(**self._config.version_option)(group)

        return group


    def _create_group(self, name, doc):
        def target(): pass
        target.__doc__ = doc
        short_help = doc_to_short_help(doc)
        name_fixed = name.replace('_', '-').rstrip('-')
        return click.group(cls=self._get_group_class(), name=name_fixed, short_help=short_help)(target)


    def _obtain_group(self, path):
        try:
            return self._groups[path]
        except KeyError:
            base_path, name = path
            base_group = self._obtain_group(base_path)
            namespace = self._galaxy[path]
            doc = namespace['__doc__']
            new_group = self._create_group(name, doc)
            base_group.add_command(new_group)
            self._groups[path] = new_group
            return new_group


    def _wrap_command(self, cmd, arg_spec_args, arg_spec_varargs, func):

        @wraps(func)
        def command_wrapper(*args, **kwargs):

            # we assume that click allways passes all the parameters and options in kwargs
            assert args == (), 'internal error'
            kwargs_ = kwargs.copy()

            # put args and varargs in a row
            varargs = kwargs_.pop(arg_spec_varargs, () )
            plain_args = tuple(kwargs_.pop(arg_name) for arg_name in arg_spec_args)
            args_ = (*plain_args, *varargs)

            # execute command with error handling
            with user_exception_guard():
                self._config.command_wrapper(cmd, args_, kwargs_)

        return command_wrapper


    def add_command(self, path, func_info):
        obj, cls = func_info
        func = extract_func(obj)
        log.debug(f"Registering function {func.__qualname__!r} as {path!r} command")

        if isclassmethod(obj):
            func_partial = partial(func, cls)
        else:
            func_partial = func

        arg_spec = inspect.getfullargspec(unwrap(func))
        arg_spec_args = arg_spec.args[int(isclassmethod(obj)):]

        all_defaults = get_all_defaults(arg_spec)

        def demangle(name):
            return name.replace('_', '-').rstrip('-')

        short_help = doc_to_short_help(getattr(func, '__doc__', None))
        cmd_opts = dict(short_help=short_help)
        cmd_opts.update(arg_spec.annotations.get('return', {}))
        command_wrapper = self._wrap_command(func_partial, arg_spec_args, arg_spec.varargs, func)
        name = demangle(func.__name__)
        cmd = click.command(name, **cmd_opts)(command_wrapper)

        def update_settings(settings, annotations):
            if isinstance(annotations, dict):
                settings.update(annotations)
            else:
                log.warning(f'Annotation of dict type expected, got {type(annotations).__name__} instead, annotation will be ignored')

        def upgrade_types(default, settings):
            type_ = settings.get('type', type(default))
            if isinstance(type_, type) and issubclass(type_, IntEnum):
                settings['type'] = IntEnumParamType(type_)

        # adding arguments
        for arg in arg_spec_args:
            required = arg not in all_defaults
            default = all_defaults.get(arg)
            log.debug(f'Arg: path={arg!r}, required={required}, default={default!r}')
            settings = dict(required=required, default=default)
            ann = arg_spec.annotations.get(arg, {})
            update_settings(settings, ann)
            upgrade_types(default, settings)
            cmd = click.argument(arg, **settings)(cmd)

        # adding options
        for opt in arg_spec.kwonlyargs:
            required = opt not in all_defaults
            default = all_defaults.get(opt)
            show_default = opt in all_defaults
            is_flag = isinstance(default, bool)
            settings = dict(required=required, default=default, show_default=show_default, is_flag=is_flag)
            ann = arg_spec.annotations.get(opt, {})
            alias = ann.pop('alias', None)
            log.debug(f'Opt: path={opt!r}, required={required}, default={default!r}, alias={alias!r}')
            if alias is not None:
                assert isinstance(alias, str), 'alias expected to be of str type'
                assert alias.startswith('-'), "alias should start with '-'"
                assert len(alias) == 2, "alias should consist of one character preceded by '-'"
            aliases = filter(None, (alias,) )
            update_settings(settings, ann)
            upgrade_types(default, settings)
            cmd = click.option(f'--{demangle(opt)}', *aliases, **settings)(cmd)

        # adding variadic arguments
        if arg_spec.varargs:
            log.debug(f'VarArgs: path={arg_spec.varargs!r}')
            settings = dict(nargs=-1)
            ann = arg_spec.annotations.get(arg_spec.varargs, {})
            update_settings(settings, ann)
            cmd = click.argument(arg_spec.varargs, **settings)(cmd)

        # checking varargs
        if arg_spec.varkw:
            log.warning(f"Kwargs are not supported, ignoring {arg_spec.varkw!r}")

        # adding command to the group
        base_path, name = path
        group = self._obtain_group(base_path)
        group.add_command(cmd)


    def run_top_group(self, app_args):
        top_group = self._groups[cmdpath.root]
        top_group(app_args, prog_name=self._prog_name)
