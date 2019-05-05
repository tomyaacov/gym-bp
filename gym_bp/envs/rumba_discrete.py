from z3 import Int, is_true, And, IntVector, Real,Not
import gym_bp.envs.global_variables as gv

# configuration
x_max = 5
y_max = 5

# variables
x = Int('x')
y = Int('y')
orientation = Int('orientation')  # 0-N, 1-E, 2-S, 3-W
#action = Int('action')
#reward = Real('reward')


def boundaries():
    while True:
        m = yield {'block': Not(And(x >= 1, x <= x_max, y >= 1, y <= y_max))}


def turn():
    m = yield {'block': orientation != 0}
    while True:
        if gv.action//10 == 1:
            direction = 2*(gv.action%10)-1
            new_orientation = (m[orientation]+direction) % 4
            m = yield {'block': Not(orientation == new_orientation)}
        else:
            m = yield {'block': Not(orientation == m[orientation])}


def move():
    m = yield {'block': Not(And(x == 1, y == 1))}
    while True:
        if gv.action//10 == 2:
            if m[orientation] == 0:
                m = yield {'block': y != m[y] + 1}
            elif m[orientation] == 1:
                m = yield {'block': x != m[x] + 1}
            elif m[orientation] == 2:
                m = yield {'block': y != m[y] - 1}
            elif m[orientation] == 3:
                m = yield {'block': x != m[x] - 1}
        else:
            m = yield {'block': Not(And(y == m[y], x == m[x]))}


def reward_def():
    m = yield {}
    while True:
        if m[x] == x_max and m[y] == y_max:
            gv.reward = 1
            m = yield {}
        else:
            gv.reward = -0.04
            m = yield {}

