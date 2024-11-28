import carRace
import gymnasium as gym
from gymnasium import spaces

import numpy as np
import pygame
import cv2
from PIL import Image
import sys


env = gym.make('carRace:carRace/NamCTrack-v0')

# obs_space = spaces.Box(np.array([0,0,0,0,0]), np.array([10,10,10,10,10]), dtype=np.uint)
# print(obs_space.high)
# print(obs_space.shape)

# NUM_BUCKETS = tuple((obs_space.high + np.ones(obs_space.shape)).astype(int))
# NUM_ACTIONS = 3
# q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS, ), dtype=float)
# print(q_table.shape)
# map_img = Image.open("track_1.png")
# print(map_img.size)
# new_width = 1500
# new_height = 800
# map_img = map_img.resize((new_width, new_height))
# map_img.save( "track_2.png")
# screen_width = 1500
# screen_height = 800

# BLACK = (0,0,0)

# if __name__ == "__main__":
    
#     pygame.init()
#     screen = pygame.display.set_mode((screen_width, screen_height))
#     clock = pygame.time.Clock()
#     race_car =  pygame.image.load("car.png")
#     race_map = pygame.image.load("track_2.png")
#     RUNNING = True
#     while RUNNING:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 RUNNING= False
#                 break
#         if not RUNNING:
#             continue
#         screen.fill(BLACK)
#         screen.blit(race_map, (0, 0))
#         pygame.display.update()
        
#     pygame.quit()
    
          
    
# if __name__ == "__main__":
    # env = gym.make("carRace/NamCEnv-v0")
    
    