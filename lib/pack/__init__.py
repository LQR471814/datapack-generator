from __future__ import annotations

import json
import os
from dataclasses import dataclass
from io import TextIOWrapper
import shutil
from typing import Any, Callable, NamedTuple, Optional, TypeAlias, TypeVar

from lib.commands import Command
from lib.common.types import ID
from semver import compare  # type: ignore

# functions

# map {<function name>:set(<compiler output hash>)}
calls: dict[str, set[int]] = {}

T = TypeVar('T', bound=Optional[NamedTuple])
MCFunction: TypeAlias = Callable[[T], ID]

class Runtime:
    lines: list[str]

    def __init__(self):
        self.lines = []

    def execute(self, c: Command):
        l = []
        for v in c.generate():
            if v is not None:
                l.append(str(v))
        self.lines.append(" ".join(l))

    def done(self, file: TextIOWrapper):
        file.write("\n".join(self.lines))
        file.close()

def mcfunction(namespace: Namespace, unique: bool = False):
    def decorator(f: Callable[[Runtime, T], None]):
        def wrapper(args: T):
            if f.__name__ not in calls:
                calls[f.__name__] = set()

            runner = Runtime()
            f(runner, args)

            if unique:
                namespace.addFunction(f.__name__, runner)
                return namespace.getID(f.__name__)

            outputHash = hash(tuple(runner.lines))
            fname = f"{f.__name__}_{outputHash}"

            if outputHash not in calls[f.__name__]:
                namespace.addFunction(fname, runner)
                calls[f.__name__].add(outputHash)

            return namespace.getID(fname)
        return wrapper
    return decorator

# pack data

@dataclass
class PackVersion:
    lower: str
    upper: str
    value: int

    def check(self, version: str) -> int | None:
        lower = compare(self.lower, version)
        upper = compare(self.upper, version)
        if lower >= 0 and upper <= 0:
            return self.value
        return None

versions = [
    PackVersion("1.13.0", "1.14.4", 4),
    PackVersion("1.15.0", "1.16.1", 5),
    PackVersion("1.16.2", "1.16.5", 6),
    PackVersion("1.17.0", "1.17.1", 7),
    PackVersion("1.18.0", "1.18.1", 8),
    PackVersion("1.18.2", "1.18.2", 9),
    PackVersion("1.19.0", "1.19.0", 9),
]

def getFormat(target: str):
    for v in versions:
        version = v.check(target)
        if version is not None:
            return version
    return

@dataclass
class PackMetadata:
    description: str
    packFormat: int

    def toJSON(self):
        return json.dumps({
            "pack": {
                "description": self.description,
                "pack_format": self.packFormat,
            }
        }, indent=4)

class Pack:
    name: str
    metadata: PackMetadata

    def __init__(self, name: str, metadata: PackMetadata):
        self.name = name

        if os.path.exists(self.name):
            shutil.rmtree(self.name)

        os.mkdir(self.name)
        os.mkdir(os.path.join(self.name, "data"))

        self.setMetadata(metadata)

    def setMetadata(self, metadata: PackMetadata):
        self.metadata = metadata

        f = open(os.path.join(self.name, "pack.mcmeta"), "w")
        f.write(self.metadata.toJSON())
        f.close()

    def getFile(self, namespace: str, path: str):
        namespacePath = os.path.join(self.name, "data", namespace)
        if not os.path.exists(namespacePath):
            os.mkdir(namespacePath)
        directory = os.path.join(namespacePath, os.path.dirname(path))
        if not os.path.exists(directory):
            os.mkdir(directory)
        return open(os.path.join(namespacePath, path), "w")

class Namespace:
    name: str
    pack: Pack

    def __init__(self, name: str, pack: Pack):
        self.name = name
        self.pack = pack

        os.mkdir(os.path.join(pack.name, "data", name))

    def __eq__(self, __o: Any):
        return self.name == __o.name

    def addFunction(self, name: str, runtime: Runtime):
        runtime.done(self.pack.getFile(self.name, f"functions/{name}.mcfunction"))

    def getID(self, name: str):
        return ID(name, self.name)

