import pygame
import random
import math
from logger import log_event
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.polygon = self.create_polygon(radius, random.randint(10, 20))
        self.current_polygon = []
    
    def create_polygon(self, radius, n):
        points = []
        for _ in range(n):
            angle = random.uniform(0, 2*math.pi)
            rad =  random.uniform(radius/2, radius)
            points.append((angle, rad))
        return sorted(points)

    def draw(self, screen):
        #pygame.draw.circle(screen, color="white", center=self.position, radius=self.radius, width=LINE_WIDTH)
        loc_adj_poly = []
        for angle, rad in self.polygon:
            vec = pygame.math.Vector2(rad, 0).rotate_rad(angle)
            x = self.position.x + vec.x
            y = self.position.y + vec.y
            loc_adj_poly.append((int(x), int(y)))
        self.current_polygon = loc_adj_poly
        pygame.draw.polygon(screen, "white", loc_adj_poly, width = LINE_WIDTH)


    def update(self, dt):
        self.position += (self.velocity * dt)

    def explosion(self):
        pass

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        split_angle = random.uniform(20, 50)
        child1_velocity = self.velocity.rotate(split_angle)
        child2_velocity = self.velocity.rotate(-split_angle)
        child_radius = self.radius - ASTEROID_MIN_RADIUS
        child_position = self.position

        child1 = Asteroid(child_position.x, child_position.y, child_radius)
        child1.velocity = child1_velocity * 1.2
        child2 = Asteroid(child_position.x, child_position.y, child_radius)
        child2.velocity = child2_velocity * 1.2
