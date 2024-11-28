import pygame
import os
import numpy as np
import gymnasium as gym
from gymnasium import spaces

from carRace.envs.race_car import RaceCar
from carRace.envs.race_track import RaceTrack

from gymnasium import spaces

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class NamCTrackEnv(gym.Env):
    metadata = {"render_modes": ["human"]}
    def __init__(self):
        self.action_space = spaces.Discrete(4) # [0,1,2,3]->[가속, 감속, 우측 steer, 좌측 steer] # 
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), 
                                            np.array([10, 10, 10, 10, 10]), dtype=np.uint)
        self.pyrace = RaceTrack()
        self.memory = []
    
    def step(self, action):
        self.pyrace.action(action)
        reward = self.pyrace.evaluate()
        done = self.pyrace.is_done()
        obs = self.pyrace.observe()
        return obs, reward, done, done, {}
    
    def reset(self):
        del self.pyrace
        self.pyrace = RaceTrack()
        obs = self.pyrace.observe()
        return obs
    
    def render(self):
        self.pyrace.view()
    
    def save_memory(self, file):
        np.save(file, self.memory)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
            
