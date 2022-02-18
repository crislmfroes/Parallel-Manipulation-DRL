#! /usr/bin/env python3

import rospy
from algorithms.bug2 import BUG2
from utils.utils import test_goals
import gym_turtlebot3
import numpy as np
import yaml
import time
import gym
import os

# Loading configs from config.yaml
path = os.path.dirname(os.path.abspath(__file__))
with open(path + '/config.yml', 'r') as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

action_low = [-1.5, -0.1]
action_high = [1.5, 0.12]
goal = None
n_agent = 0
local_episode = 0
agent = BUG2()

goal = [test_goals(local_episode)]
rospy.init_node(config['env_name'].replace('-', '_') + "_w{}".format(n_agent))
env = gym.make(config['env_name'], env_stage=config['env_stage'], observation_mode=0, continuous=True, goal_list=goal)
time.sleep(1)

best_reward = -float("inf")
rewards = []
while local_episode <= config['test_trials']:
    episode_reward = 0
    num_steps = 0
    local_episode += 1
    ep_start_time = time.time()
    goal = [test_goals(local_episode)]
    print("New Goal:", goal)
    state = env.reset(new_random_goals=False, goal=goal)
    done = False
    while not done:
        for s in range(len(state)):
            if state[s] > 2.5:
                state[s] = 2.5

        action = agent.get_action(state)
        print('Action:', action)
        action[0] = np.clip(action[0], action_low[0], action_high[0])
        action[1] = np.clip(action[1], action_low[1], action_high[1])

        next_state, reward, done, info = env.step(action)
        episode_reward += reward
        state = next_state

        if done or num_steps == config['max_ep_length']:
            break

        num_steps += 1
        position = env.get_position()  # Get x and y turtlebot position to compute test charts
        # logs[3] = position[0]
        # logs[4] = position[1]

    # Log metrics
    episode_timing = time.time() - ep_start_time
    print(f"Agent: [{n_agent}/{config['num_agents'] - 1}] Episode: [{local_episode}/"
          f"{config['test_trials']}] Reward: "
          f"[{episode_reward}/200] Step: {num_steps} Episode Timing: {round(episode_timing, 2)}s")

    # logs[0] = episode_reward
    # logs[1] = episode_timing
    # logs[2] = local_episode

print(f"Agent {n_agent} done.")