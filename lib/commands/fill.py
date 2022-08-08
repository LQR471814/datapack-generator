from dataclasses import dataclass
from typing import Optional

from lib.commands import Command
from lib.common.types import Position, SEnum


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

    def generate(self):
        return ["fill", self.fromPos, self.toPos, self.block, self.option, self.replaceFilter]
