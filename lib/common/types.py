from dataclasses import dataclass
from enum import Enum
from typing import Optional

from lib.common.nbt import NBT


class SEnum(Enum):
    def __str__(self):
        return str(self.value)

@dataclass
class AbsolutePosition:
    x: int
    y: int
    z: int

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

@dataclass
class RelativePosition:
    x: int = 0
    y: int = 0
    z: int = 0

    def __str__(self):
        x = f"~{self.x}" if self.x != 0 else "~"
        y = f"~{self.y}" if self.y != 0 else "~"
        z = f"~{self.z}" if self.z != 0 else "~"
        return f"{x} {y} {z}"

Position = AbsolutePosition | RelativePosition

class TargetSelector(SEnum):
    nearestPlayer = "@p"
    randomPlayer = "@r"
    allPlayers = "@a"
    allEntities = "@e"
    executor = "@s"

Target = str | TargetSelector

class Storage:
    def __str__(self):
        return "storage"

class Effect(SEnum):
    speed = "speed"
    slowness = "slowness"
    haste = "haste"
    miningFatigue = "mining_fatigue"
    strength = "strength"
    instantHealth = "instant_health"
    instantDamage = "instant_damage"
    jumpBoost = "jump_boost"
    nausea = "nausea"
    regeneration = "regeneration"
    resistance = "resistance"
    fireResistance = "fire_resistance"
    waterBreathing = "water_breathing"
    invisibility = "invisibility"
    blindness = "blindness"
    nightVision = "night_vision"
    hunger = "hunger"
    weakness = "weakness"
    poison = "poison"
    wither = "wither"
    healthBoost = "health_boost"
    absorption = "absorption"
    saturation = "saturation"
    glowing = "glowing"
    levitation = "levitation"
    luck = "luck"
    badLuck = "bad_luck"
    slowFalling = "slow_falling"
    conduitPower = "conduit_power"
    dolphinsGrace = "dolphins_grace"
    badOmen = "bad_omen"
    heroOfTheVillage = "hero_of_the_village"
    darkness = "darkness"

@dataclass
class ID:
    name: str
    namespace: str = "minecraft"

    def __str__(self):
        return f"{self.namespace}:{self.name}"

@dataclass
class BlockState:
    blockID: ID
    states: dict[str, str]
    tags: Optional[NBT] = None

    def __str__(self):
        pairs: list[str] = []
        for k in self.states:
            pairs.append(f"{k}={self.states[k]}")
        states = ",".join(pairs)
        return f"{self.blockID}[{states}]{{{self.tags}}}"

class TimeUnit(SEnum):
    day = "d"
    second = "s"
    tick = ""

@dataclass
class Time:
    amount: float
    unit: TimeUnit

    def __str__(self):
        return f"{self.amount}{self.unit}"
