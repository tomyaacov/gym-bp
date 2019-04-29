import gym
from gym import error, spaces, utils
from gym.utils import seeding
from z3 import *
import gym_bp.envs.global_variables as gv
from gym_bp.envs.bprogram import Bprogram
from random import randint, choice


class BPEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.bprogram = Bprogram()
        self.source_name = None
        self.np_random = None

    def step(self, action):
        print(action)
        self.bprogram.trigger_action(action)
        done = self.bprogram.trigger_next_state()
        state = [gv.m[self.bprogram.variables[x]] for x in self.bprogram.variables if x not in ['action', 'reward']]
        reward = gv.m[self.bprogram.variables['reward']]
        print(state, reward)
        return state, float(reward.as_decimal(3)), done, {}

    def reset(self):
        self.bprogram.setup(source_name=self.source_name)
        state = [gv.m[self.bprogram.variables[x]] for x in self.bprogram.variables if x not in ['action', 'reward']]
        print(state)
        return state

    def render(self, mode='human', close=False):
        raise NotImplementedError

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


if __name__ == "__main__":
    env = BPEnv()
    env.source_name = "rumba_discrete"
    observation = env.reset()
    for _ in range(100):
        # env.render()
        action = choice([10,11,20])
        observation, reward, done, info = env.step(action)
        if done:
            # observation = env.reset()
            break
    env.close()
