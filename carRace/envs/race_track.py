from carRace.envs.race_car import (
    RaceCar, screen_width, screen_height, corners, #  car_pos
)

import pygame

class RaceTrack:
    CAR_START_POS = [1235, 200]
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.CAR_START_POS = [1235, 200]
        print(self.CAR_START_POS)
        self.car = RaceCar(car_file='car.png',
                           map_file='track_2.png',
                           pos=self.CAR_START_POS)
        print("CAR POS ", self.car.pos, self.car.angle, self.car.speed)
        self.game_speed = 60
        self.mode = 0
    
    def action(self, action):
        if action == 0:
            self.car.speed += 2
        elif action == 3:
            self.car.speed -= 2
        if action == 1:
            self.car.angle += 5
        elif action == 2:
            self.car.angle -= 5
        
        self.car.update()
        self.car.check_collision()
        self.car.check_corner()
        self.car.radars.clear()
        for d in range(-90, 120, 45):
            self.car.check_radar(d)
    
    def evaluate(self):
        reward = 0
        if not self.car.is_alive:
            reward = -1000000 + self.car.distance
        
        elif self.car.goal:
            reward = 1000000
        return reward

    def is_done(self):
        if not self.car.is_alive or self.car.goal:
            self.car.current_check = 0
            self.car.distance = 0
            return True
        return False
    
    def observe(self):
        radars = self.car.radars
        ret = [0, 0, 0, 0, 0]
        for i, r in enumerate(radars):
            radar_pos, radar_dist = r
            ret[i] = int(radar_dist / 20)
        return ret
    
    def view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.mode += 1
                    self.mode = self.mode % 3
                    
        self.screen.blit(self.car.map, (0, 0))
        if self.mode == 1:
            self.screen.fill((0, 0, 0))
            
        self.car.radars_for_draw.clear()
        for d in range(-90, 105, 15):
            self.car.check_radar_for_draw(d)
        pygame.draw.circle(self.screen, (255, 255, 0), corners[self.car.current_check], 70, 1)
        self.car.draw_collision(self.screen)
        self.car.draw_radar(self.screen)
        self.car.draw(self.screen)
        
        pygame.display.flip()
        self.clock.tick(self.game_speed)
        
    