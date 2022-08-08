from dataclasses import dataclass

@dataclass
class Command:
    def generate(self) -> list[list] | list:
        return []
