from enum import IntEnum
import click

class Hex(int):

    def __new__(cls, value):
        if isinstance(value, str):
            if value[:2].lower() != "0x":
                raise ValueError(f'invalid literal for {cls.__name__}(): {value}')
            value = int(value, 16)
        return int.__new__(cls, value)

    def __repr__(self):
        return hex(self)

    def __str__(self):
        return repr(self)

class HexParamType(click.ParamType):
    name = "hexadecimal integer"

    def convert(self, value, param, ctx):
        try:
            return Hex(value)
        except (ValueError):
            self.fail(f"{value!r} is not a valid {self.name}", param, ctx)

HEX = HexParamType()

class AlternativesParamType(click.ParamType):
    def __init__(self, *types):
        self.types = types
        self.name = ' or '.join(t.name for t in self.types)
        super().__init__()

    def convert(self, value, param, ctx):
        for t in self.types:
            try:
                return t.convert(value, param, ctx)
            except click.BadParameter as exc:
                pass
        raise self.fail(f"{value!r} is not a valid {self.name}", param, ctx)

HEXDEC = AlternativesParamType(click.INT, HEX)

class IntEnumParamType(click.Choice):

    def __init__(self, int_enum):
        assert issubclass(int_enum, IntEnum)
        self.int_enum = int_enum
        self.name = self.int_enum.__name__
        super().__init__({i.name: i.value for i in int_enum})

    def convert(self, value, param, ctx):
        try:
            name = super().convert(value, param, ctx)
            return self.int_enum[name]
        except (click.BadParameter, KeyError):
            try:
                value = HEXDEC.convert(value, param, ctx)
                return self.int_enum(value)
            except (click.BadParameter, ValueError):
                raise self.fail(f"{value!r} is not a valid {self.name}", param, ctx)

