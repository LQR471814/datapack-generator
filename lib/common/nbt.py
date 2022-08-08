from __future__ import annotations

from dataclasses import dataclass
from typing import Any

class byte(int):
    pass
class short(int):
    pass
class long(int):
    pass
class double(int):
    pass

class byteArray(list[int]):
    pass
class intArray(list[int]):
    pass
class longArray(list[int]):
    pass

NBTValue = (
    bool | str | int | float |
    byte | short | long | double |
    list | dict[str, Any] | bytes |
    byteArray | intArray | longArray
)

@dataclass
class NBT:
    nbt: dict[str, NBTValue]

    def serialize(self, value: NBTValue):
        match value:
            case bool():
                return str(value).lower()
            case str():
                return f"'{value}'"
            case int():
                return str(value)
            case float():
                return f"{value}f"
            case byte():
                return f"{value}b"
            case short():
                return f"{value}s"
            case long():
                return f"{value}l"
            case double():
                return f"{value}d"
            case list():
                prefix = ""
                match value:
                    case byteArray():
                        prefix = "B;"
                    case intArray():
                        prefix = "I;"
                    case longArray():
                        prefix = "L;"

                values: list[str] = []
                for v in value:
                    values.append(self.serialize(v))
                result = ",".join(values)

                return f"[{prefix}{result}]"
            case dict():
                self.serialize(value)

    def __str__(self):
        return self.serialize(self.nbt)
