import inspect


def isstaticmethod(obj):
    return isinstance(obj, staticmethod)


def getfile(obj):
    """ The same as inspect.getfile, but also supports static methods
    """
    if isinstance(obj, staticmethod):
        return getfile(obj.__func__)
    else:
        return inspect.getfile(obj)


def get_all_defaults(full_arg_spec):
    """ Get cumulative dictionary of default values for all args & kwargs
    """
    defaults = full_arg_spec.defaults or ()
    kwonly_defaults = full_arg_spec.kwonlydefaults or {}
    args_defaults = dict(zip(reversed(full_arg_spec.args), reversed(defaults)))
    all_defaults = {**args_defaults, **kwonly_defaults}
    return all_defaults


def unwrap(func):
    """ Unwrap function wrapped by another one, decorated by functools.wraps
    """
    if hasattr(func, '__wrapped__'):
        return unwrap(func.__wrapped__)
    else:
        return func
