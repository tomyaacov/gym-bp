import gym
from gym import error, spaces, utils
from gym.utils import seeding


class BPEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def render(self, mode='human', close=False):
        raise NotImplementedError

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
