from collections import namedtuple

from lib.commands.fill import Fill
from lib.commands.schedule import Schedule, ScheduleFunction, ScheduleMode
from lib.common.types import RelativePosition, Time, TimeUnit
from lib.pack import Namespace, Pack, PackMetadata, Runtime, getFormat, mcfunction

pack = Pack("output", PackMetadata("output datapack", getFormat("1.19.0")))
namespace = Namespace("output", pack)

FillArgs = namedtuple("FillArgs", ["index", "scale"])

@mcfunction(namespace)
def fill(r: Runtime, args: FillArgs):
    r.execute(Fill(
        RelativePosition(0, (-args.index) * args.scale, 0),
        RelativePosition(40, (-args.index + 1) * args.scale, 40),
        "minecraft:lava"
    ))

@mcfunction(namespace, preserve_name=True)
def main(r: Runtime, args: None):
    for i in range(3):
        r.execute(Schedule(ScheduleFunction(
            functionID=fill(FillArgs(i, 60)),
            time=Time(1, TimeUnit.second),
            mode=ScheduleMode.append,
        )))

if __name__ == "__main__":
    main(None)
