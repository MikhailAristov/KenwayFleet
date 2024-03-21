class Ship:

    name: str
    level: int
    speed: float
    firepower: float
    hit_points: float
    max_hp: float

    def __init__(self, name: str, stats):
        self.name = name
        self.level = stats['level']
        self.speed = stats['speed']
        self.firepower = stats['fire']
        self.max_hp = stats['maxhp']
        self.hit_points = self.max_hp

    def fire(self, at: 'Ship'):
        pass

    def take_damage(self, attacker: 'Ship'):
        self.hit_points = max(0., self.hit_points - attacker.firepower)
