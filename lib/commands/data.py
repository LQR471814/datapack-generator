from dataclasses import dataclass
from typing import Optional

from lib.commands import Command
from lib.common.nbt import NBT
from lib.common.types import AbsolutePosition, RelativePosition, SEnum, Storage, Target

Source = RelativePosition | AbsolutePosition | Target | Storage

# Get

@dataclass
class Get(Command):
    target: Source
    path: Optional[str] = None
    scale: Optional[int] = None

    def generate(self):
        return ["get", self.target, self.path, self.scale]

# Merge

@dataclass
class Merge(Command):
    target: Source
    nbt: NBT

    def generate(self):
        return ["merge", self.target, self.nbt]

# Modify

class ModifyAction(SEnum):
    append = "append"
    insert = "insert"
    merge = "merge"
    prepend = "prepend"
    set = "set"

@dataclass
class ModifyFrom(Command):
    source: Source
    path: Optional[str] = None

    def generate(self):
        return ["from", self.source, self.path]

@dataclass
class ModifyValue(Command):
    value: int

    def generate(self):
        return ["value", self.value]

@dataclass
class Modify(Command):
    target: Source
    nbt: NBT
    action: ModifyAction
    value: ModifyFrom | ModifyValue

    def generate(self):
        return ["merge", self.target, self.nbt, self.action, *self.value.generate()]

# Remove

@dataclass
class Remove(Command):
    target: Source
    path: Optional[str] = None

    def generate(self):
        return ["remove", self.target, self.path]

# Data

@dataclass
class Data(Command):
    action: Get | Merge | Modify | Remove

    def generate(self):
        return ["data", *self.action.generate()]
