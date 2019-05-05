import gym
from gym import error, spaces, utils
from gym.utils import seeding
from z3 import *
import gym_bp.envs.global_variables as gv
from random import randint, choice


class BPEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.bprogram = None
        self.np_random = None
        self.last_event = None

    def step(self, action):
        print(action)
        gv.action = action
        self.bprogram.advance_bthreads(self.last_event)
        self.last_event = self.bprogram.next_event()
        if self.last_event is None:
            print("done", reward)
            return None, gv.reward, True, {}
        else:
            state = [self.last_event[self.bprogram.variables[x]] for x in self.bprogram.variables if x not in ['action', 'reward']]
            print(state, gv.reward)
            return state, gv.reward, False, {}

    def reset(self):
        self.last_event = None
        self.bprogram.setup()
        self.last_event = self.bprogram.next_event()
        state = [self.last_event[self.bprogram.variables[x]] for x in self.bprogram.variables if x not in ['action', 'reward']]
        print(state)
        return state

    def render(self, mode='human', close=False):
        raise NotImplementedError

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def set_bprogram(self, bprogram):
        self.bprogram = bprogram

import sys
sys.path.append("/Users/tomyaacov/Desktop/university/thesis/BPpy")
from model.bprogram import Bprogram
from execution.listeners.print_b_program_runner_listener import PrintBProgramRunnerListener
from model.event_selection.smt_event_selection_strategy import SMTEventSelectionStrategy
from model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy

if __name__ == "__main__":
    bprogram =Bprogram(source_name="rumba_discrete",
                       event_selection_strategy=SMTEventSelectionStrategy(),
                       listener=PrintBProgramRunnerListener())
    env = BPEnv()
    env.set_bprogram(bprogram)
    observation = env.reset()
    for _ in range(100):
        # env.render()
        action = choice([10,11,20])
        observation, reward, done, info = env.step(action)
        if done:
            # observation = env.reset()
            break
    env.close()
