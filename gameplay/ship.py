class Ship:

    name: str
    level: int
    speed: float
    firepower: float
    max_hp: float

    cooldown: float
    hit_points: float

    def __init__(self, name: str, stats):
        self.name = name
        self.level = stats['level']
        self.speed = stats['speed']
        self.firepower = stats['fire']
        self.max_hp = stats['maxhp']
        self.cooldown = 1.
        self.hit_points = self.max_hp

    def fire(self, at: 'Ship'):
        pass

    def take_damage(self, attacker: 'Ship'):
        self.hit_points = max(0., self.hit_points - attacker.firepower)

    def __str__(self) -> str:
        return "{0:} ({3:.2f}, {1:.0f}/{2:.0f})".format(self.name, self.hit_points, self.max_hp, self.cooldown)

    def cool(self, steps: float):
        self.cooldown = max(0., self.cooldown - self.speed / 1000 * steps)

    @property
    def remaining_steps(self):
        return self.cooldown * 1000 / self.speed

    def reset_cooldown(self):
        self.cooldown = 1.
