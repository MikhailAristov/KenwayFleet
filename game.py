from data import ships
from gameplay import Ship


def play():
    print("game played!")
    _ = Ship('gunboat01', ships['gunboat01'])


if __name__ == '__main__':
    play()
