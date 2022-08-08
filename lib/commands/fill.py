from dataclasses import dataclass
import math
from typing import Optional

from lib.commands import Command
from lib.common.general import clamp_abs
from lib.common.types import Position, RelativePosition, SEnum
from lib.common.logs import command_warning

fillmax = 32768
sidemax = 32

class FillOption(SEnum):
    destroy = "destroy"
    hollow = "hollow"
    keep = "keep"
    outline = "outline"
    replace = "replace"

@dataclass
class Fill(Command):
    fromPos: Position
    toPos: Position
    block: str
    option: Optional[FillOption] = None
    replaceFilter: Optional[str] = None
    autoFragment = True

    def generate(self):
        dynamic = (
            type(self.fromPos) is Position and
            type(self.toPos) is RelativePosition
        ) or (
            type(self.fromPos) is RelativePosition and
            type(self.toPos) is Position
        )

        if dynamic:
            command_warning(
                "fill", "autofragmenting and volume checks are not possible while",
                "using an absolute position and relative position together"
            )
            return ["fill", self.fromPos, self.toPos, self.block, self.option, self.replaceFilter]

        difference = self.fromPos.difference(self.toPos)
        volume = difference.volume()
        if not self.autoFragment and volume > 32768:
            command_warning(
                "fill", f"will fail because the specified range has a volume ({volume})",
                "more than 32768 blocks and auto fragmenting has been turned off"
            )
            return []

        abs_difference = difference.abs()

        commands: list[list] = []
        for x in range(math.ceil(abs_difference.x / sidemax)):
            for y in range(math.ceil(abs_difference.y / sidemax)):
                for z in range(math.ceil(abs_difference.z / sidemax)):
                    fromPos = RelativePosition(x * sidemax, y * sidemax, z * sidemax)
                    toPos = RelativePosition(
                        clamp_abs((x + 1) * sidemax, abs_difference.x),
                        clamp_abs((y + 1) * sidemax, abs_difference.y),
                        clamp_abs((z + 1) * sidemax, abs_difference.z),
                    )

                    if isinstance(self.fromPos, Position):
                        fromPos = fromPos.add(self.fromPos)
                        toPos = toPos.add(self.toPos)

                    commands.append(
                        ["fill", fromPos, toPos, self.block, self.option, self.replaceFilter]
                    )

        return commands
