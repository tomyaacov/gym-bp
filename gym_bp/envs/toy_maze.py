from z3 import Int, is_true, And
import gym_bp.envs.global_variables as gv

x = Int('x')
y = Int('y')
action = Int('action')
reward = Int('reward')


def vertical():
    yield {'must': y == 2, 'wait-for': y == 2}
    while True:
        if gv.action == 1:
            yield {'must': y == gv.m[y] + 1, 'wait-for': y == gv.m[y] + 1}
        elif gv.action == 3:
            yield {'must': y == gv.m[y] - 1, 'wait-for': y == gv.m[y] - 1}
        else:
            yield {'must': y == gv.m[y], 'wait-for': y == gv.m[y]}


def horizontal():
    yield {'must': x == 2, 'wait-for': x == 2}
    while True:
        if gv.action == 2:
            yield {'must': x == gv.m[x] + 1, 'wait-for': x == gv.m[x] + 1}
        elif gv.action == 4:
            yield {'must': x == gv.m[x] - 1, 'wait-for': x == gv.m[x] - 1}
        else:
            yield {'must': x == gv.m[x], 'wait-for': x == gv.m[x]}


def boundaries():
    while True:
        yield {'must': And(x >= 1, x <= 3, y >= 1, y <= 3)}
