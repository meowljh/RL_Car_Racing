import pygame
import math
import numpy as np
from carRace.envs.utils import rot_center, get_distance

WHITE = (255, 255, 255, 255) # 배경이 white이기 때문에, 도로 위가 아닌 경우 check를 하기 위함 #
GREEN = (0, 255, 0)

screen_width = 1500 # 1152
screen_height = 800 # 489
car_pos = [1235, 200]
corners = [
    (800, 110),
    (175, 600),
    (560, 400),
    (925, 645),
    (1085, 490),
    (1440, 365)
][::-1]

class RaceCar:
    def __init__(self, car_file, map_file, pos):
        self.surface = pygame.image.load(car_file)
        self.map = pygame.image.load(map_file)
        self.surface = pygame.transform.scale(self.surface, (80, 80))
        self.rotate_surface = self.surface
        self.width, self.height = self.rotate_surface.get_size()

        self.pos = pos
        self.angle = 0 # yaw angle based on the steering wheel #
        self.speed = 0
        self.center = [self.pos[0] + 40, self.pos[1] + 40]
        self.radars = []
        self.radars_for_draw = []
        self.is_alive = True
        self.current_check = 0
        self.prev_distance = 0
        self.cur_distance = 0
        self.goal = False
        self.check_flag = False
        self.distance = 0
        self.time_spent = 0

        for d in range(-90, 120, 45):
            self.check_radar(d)
        
        for d in range(-90, 105, 15):
            self.check_radar_for_draw(d)
    
    def update(self):
        self.speed -= 0.5
        self.speed = np.clip(self.speed, 1, 10) # a_min을 1로 둬서 멈추는 것 방지 #
        self.rotate_surface = rot_center(self.surface, self.angle) # rotate the vehicle to match the yaw angle #
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        
        self.pos[0] = np.clip(self.pos[0], a_min=20, a_max=screen_width - 120)
        self.pos[1] = np.clip(self.pos[1], a_min=20, a_max=screen_height - 120)
        
        self.distance += self.speed
        self.time_spent += 1
        
        self.center = [int(self.pos[0]) + 40, int(self.pos[1]) + 40]
        print("pos ", self.pos)
        print("center ", self.center)
        len = 40
        self.four_points = []
        for angle in [30, 150, 210, 330]:
            self.four_points.append(
                [self.center[0] + math.cos(math.radians(360 - (self.angle + angle))) * len, \
                    self.center[1] + math.sin(math.radians(360 - (self.angle + angle))) * len]
            ) # track의 바깥으로 나갈 수 있으니 막기 위해서 확인 #
        
    
    def check_collision(self):
        self.is_alive = True
        for p in self.four_points:
            if self.map.get_at((int(p[0]), int(p[1]))) == WHITE:
                self.is_alive = False
                break
    
    def check_corner(self):
        p = corners[self.current_check]
        self.prev_distance = self.cur_distance
        dist = get_distance(p, self.center)
        if dist < 70:
            self.current_check += 1
            self.prev_distance = 99999
            self.check_flag = True
            if self.current_check > len(corners) - 1:
                self.current_check = 0
                self.goal = True
            else:
                self.goal = False
        self.cur_distance = dist
    
    def in_range(self, x, y):
        width, height = self.rotate_surface.get_size()
        return 0 <= x < width and 0 <= y < height
    
    def check_radar(self, deg):
        len = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + deg))) * len)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + deg))) * len)
        
        # while self.in_range(x, y) and not self.map.get_at((x, y)) == WHITE and len < 200:
        while not self.map.get_at((x, y)) == WHITE and len < 200: 
            len += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + deg))) * len)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + deg))) * len)
        
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def check_radar_for_draw(self, deg):
        len = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + deg))) * len)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + deg))) * len)
        
        # while self.in_range(x, y) and not self.map.get_at((x, y)) == WHITE and len < 200:
        while not self.map.get_at((x, y)) == WHITE and len < 2000: 
            len += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + deg))) * len)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + deg))) * len)
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars_for_draw.append([(x, y), deg])
        
    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)
    
    def draw_collision(self, screen):
        for i in range(4):
            x = int(self.four_points[i][0])
            y = int(self.four_points[i][1])
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)
    
    def draw_radar(self, screen):
        for r in self.radars_for_draw:
            pos, dist = r
            pygame.draw.line(screen, color=GREEN, start_pos=self.center, end_pos=pos, width=1)
            pygame.draw.circle(screen, color=GREEN, center=pos, radius=5)
    