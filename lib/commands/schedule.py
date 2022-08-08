from dataclasses import dataclass

from lib.commands import Command
from lib.common.types import ID, SEnum, Time


class ScheduleMode(SEnum):
    append = "append"
    replace = "replace"

@dataclass
class ScheduleFunction(Command):
    functionID: ID
    time: Time
    mode: ScheduleMode

    def generate(self):
        return ["function", self.functionID, self.time, self.mode]

@dataclass
class ScheduleClear(Command):
    functionID: ID

    def generate(self):
        return ["clear", self.functionID]

@dataclass
class Schedule(Command):
    action: ScheduleFunction | ScheduleClear

    def generate(self):
        return ["schedule", *self.action.generate()]
