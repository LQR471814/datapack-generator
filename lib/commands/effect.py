from dataclasses import dataclass
from typing import Optional

from lib.commands import Command
from lib.common.types import Effect, Target


@dataclass
class Clear(Command):
    target: Target
    effect: Effect

    def generate(self):
        return ["clear", self.target, self.effect]

@dataclass
class Give(Command):
    target: Target
    effect: Effect
    seconds: Optional[int] = None # -1 will be treated as infinite
    amplifier: Optional[int] = None # a number from 1 - 255
    hideParticles: Optional[bool] = None

    def generate(self):
        return [self.target, self.effect, self.seconds, self.amplifier, self.hideParticles]

@dataclass
class Affect(Command):
    action: Clear | Give

    def generate(self):
        return ["effect", *self.action.generate()]
