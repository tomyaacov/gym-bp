import numpy as np
import random
import operator
from gym_bp.envs.bp_env import BPEnv

env = BPEnv()
env.source_name = "rumba_discrete"
q_table = {}


# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1
actions = [10,11,20]
episodes_num = 20

# For plotting metrics
all_epochs = []
all_penalties = []

for i in range(1, episodes_num+1):
    state = env.reset()

    epochs, penalties, reward, = 0, 0, 0
    done = False

    while not done:

        if tuple(state) not in q_table:
            q_table[tuple(state)] = {}
            for action in actions:
                q_table[tuple(state)][action] = 0

        if random.uniform(0, 1) < 1-(i/episodes_num):
            action = random.choice(actions)  # Explore action space
        else:
            action = max(q_table[tuple(state)].items(), key=operator.itemgetter(1))[0]  # Exploit learned values

        next_state, reward, done, info = env.step(action)

        old_value = q_table[tuple(state)][action]
        next_max = max(q_table[tuple(state)].items(), key=operator.itemgetter(1))[1]

        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[tuple(state)][action] = new_value

        if reward == -10:
            penalties += 1

        state = next_state
        epochs += 1

    if i % 10 == 0:
        #clear_output(wait=True)
        print("Episode: {}".format(i))

print("Training finished.\n")
print(q_table)

state = env.reset()
done = False

while not done:
    action = max(q_table[tuple(state)].items(), key=operator.itemgetter(1))[0]
    state, reward, done, info = env.step(action)