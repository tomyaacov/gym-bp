from z3 import Int, is_true, And, IntVector, Real
import gym_bp.envs.global_variables as gv

# configuration
x_max = 5
y_max = 5

# variables
x = Int('x')
y = Int('y')
orientation = Int('orientation')  # 0-N, 1-E, 2-S, 3-W
action = Int('action')
reward = Real('reward')


def boundaries():
    while True:
        yield {'must': And(x >= 1, x <= x_max, y >= 1, y <= y_max)}


def turn():
    yield {'must': orientation == 0, 'wait-for': orientation == 0}
    while True:
        if gv.action//10 == 1:
            direction = 2*(gv.action%10)-1
            yield {'must': orientation == (gv.m[orientation]+direction) % 4, 'wait-for': x > 0}
        else:
            yield {'must': orientation == gv.m[orientation], 'wait-for': x > 0}


def move():
    yield {'must': And(x == 1, y == 1), 'wait-for': And(x == 1, y == 1)}
    while True:
        if gv.action//10 == 2:
            if gv.m[orientation] == 0:
                yield {'must': y == gv.m[y] + 1, 'wait-for': y == gv.m[y] + 1}
            elif gv.m[orientation] == 1:
                yield {'must': x == gv.m[x] + 1, 'wait-for': x == gv.m[x] + 1}
            elif gv.m[orientation] == 2:
                yield {'must': y == gv.m[y] - 1, 'wait-for': y == gv.m[y] - 1}
            elif gv.m[orientation] == 3:
                yield {'must': x == gv.m[x] - 1, 'wait-for': x == gv.m[x] - 1}
        else:
            yield {'must': And(y == gv.m[y], x == gv.m[x]), 'wait-for': x > 0}


def reward_def():
    yield {'wait-for': x > 0}
    while True:
        if gv.m[x] == x_max and gv.m[y] == y_max:
            yield {'must': reward == 1, 'wait-for': x > 0}
        else:
            yield {'must': reward == -0.04, 'wait-for': x > 0}

