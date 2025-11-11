import pygame
import matplotlib.path as mpltPath
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cd = 0
        self.score = 0
        self.velocity = pygame.Vector2(0,0)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(surface=screen, 
                            color="pink", 
                            points=self.triangle(), 
                            width=LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def add_speed(self, dt):
        input_velocity = pygame.Vector2(0, PLAYER_ACCELERATION * dt).rotate(self.rotation)
        self.velocity += input_velocity

    def move(self):
        self.position += (self.velocity)
        self.velocity *= PLAYER_DRAG
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT


    def shoot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity *= PLAYER_SHOOT_SPEED

    def increase_score(self):
        self.score += 1

    def collides_with(self, asteroid):
        print(f"Triangle points: {self.triangle()}\nPolygon: {asteroid.current_polygon}")
        danger_zone = mpltPath.Path(asteroid.current_polygon)
        return danger_zone.contains_points(self.triangle()).any()

    def update(self, dt):
        self.shot_cd -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.add_speed(dt)
        if keys[pygame.K_s]:
            self.add_speed(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            if self.shot_cd <= 0:
                self.shoot()
                self.shot_cd = PLAYER_SHOOT_COOLDOWN_SECONDS
        self.move()
