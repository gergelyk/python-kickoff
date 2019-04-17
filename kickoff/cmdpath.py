
class CmdPath:
    """Hashable path"""

    def __init__(self):
        self._tuple = tuple()

    def __hash__(self):
        return hash(self._tuple)

    def __eq__(self, other):
        return self._tuple == other._tuple

    def __str__(self):
        return '.'.join(self._tuple)

    def __repr__(self):
        return repr(str(self))

    def append(self, leaf):
        p = CmdPath()
        p._tuple = (*self._tuple, leaf)
        return p

    def __truediv__(self, leaf):
        return self.append(leaf)

    def split(self):
        *base_, leaf = self._tuple
        p = CmdPath()
        p._tuple = tuple(base_)
        return p, leaf

    def __iter__(self):
        yield from self.split()


root = CmdPath()

