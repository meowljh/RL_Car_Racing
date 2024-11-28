import pygame
import gymnasium as gym

env = gym.make("CarRacing-v1", domain_randomize=True)
env.reset()


# import gym

# env = gym.make("LunarLander-v2", render_mode="human")
# observation, info = env.reset()

# for _ in range(1000):
#     action = env.action_space.sample() # agent policy that uses the observation and info #
#     print("Action ", action)
#     observation, reward, terminated, truncated, info = env.step(action)
#     print("Reward ", reward)
#     if terminated or truncated:
#         observation, info = env.reset()
# env.close()