from dataclasses import dataclass


@dataclass
class ShipData:
    level: int
    speed: float
    fire: float
    hp: float
    cooldown: float

    def copy_values(self, other: 'ShipData'):
        self.level = other.level
        self.speed = other.speed
        self.fire = other.fire
        self.hp = other.hp
        self.cooldown = other.cooldown


class Ship:
    name: str
    level: int
    speed: float
    firepower: float
    max_hp: float

    cooldown: float
    hit_points: float

    def __init__(self, name: str, stats: dict):
        self.name = name
        self.level = stats['level']
        self.speed = stats['speed']
        self.firepower = stats['fire']
        self.max_hp = stats['max_hp']
        self.hit_points = self.max_hp
        self.reset_cooldown()

    def fire(self, target: 'Ship'):
        target.take_damage(self.firepower)

    def take_damage(self, amount: float):
        self.hit_points = max(0., self.hit_points - amount)

    def __str__(self) -> str:
        return "{0:} ({3:.2f}, {1:.0f}/{2:.0f})".format(self.name, self.hit_points, self.max_hp, self.cooldown)

    def cool(self, steps: float):
        self.cooldown = max(0., self.cooldown - self.speed / 1000 * steps)

    @property
    def remaining_steps(self) -> float:
        return self.cooldown * 1000 / self.speed

    def reset_cooldown(self):
        self.cooldown = 1.

    @property
    def is_sunk(self) -> bool:
        return self.hit_points <= 0

    @property
    def data(self) -> ShipData:
        return ShipData(self.level, self.speed, self.firepower, self.hit_points, self.cooldown)
