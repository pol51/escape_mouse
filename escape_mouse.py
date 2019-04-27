from enum import IntFlag, IntEnum
import pygame
import time
from pygame.math import Vector2

CASE_SIZE = 96

class Item(IntFlag):
  WALL = 0
  PATH = 1
  MOUSE = 2
  CAT = 4
  GOAL = 8
  
class Move:
  LEFT = Vector2(-1, 0)
  RIGHT = Vector2(1, 0)
  UP = Vector2(0, -1)
  DOWN = Vector2(0, 1)

world = [
  [0,0,0,0,0,0,0,0,0,0],
  [0,5,0,1,1,1,1,0,9,0],
  [0,1,0,1,0,0,1,0,1,0],
  [0,1,0,1,0,0,1,0,1,0],
  [0,3,0,1,0,0,1,0,1,0],
  [0,1,0,1,0,0,1,0,1,0],
  [0,1,0,1,0,0,1,0,1,0],
  [0,1,0,1,0,0,1,0,1,0],
  [0,1,1,1,0,0,1,1,1,0],
  [0,0,0,0,0,0,0,0,0,0]
]


class Persona:
    def __init__(self, img, pos=Vector2(0, 0)):
        sprite = pygame.image.load(img)
        self.sprite = pygame.transform.scale(sprite, (CASE_SIZE, CASE_SIZE))
        self.pos = pos
        self.follower = None
        self.moves = []
        
    def follow(self, other, path_to_other):
        self.moves = path_to_other
        other.follower = self

    def draw(self, screen):
        screen.blit(self.sprite, (self.pos.x * CASE_SIZE, self.pos.y * CASE_SIZE))
        
    def move(self, move):
        pos = self.pos + move
        if world[int(pos.y)][int(pos.x)] & Item.PATH:
            self.pos = pos
            if self.follower:
                self.follower.moves.append(move)
        if self.follower:
            self.follower.move_next()
            
    def move_next(self):
        if len(self.moves):
          move, *self.moves = self.moves
          self.move(move)
          
            
def get_init_world_position(flag):
  for i in range(len(world)):
      for j in range(len(world[i])):
          if world[i][j] & flag:
              return Vector2(j, i)


def blur_surface(surface, radius):
    from PIL import Image, ImageFilter
    pil_blured = Image.frombytes('RGBA', surface.get_size(), pygame.image.tostring(surface, 'RGBA')).filter(ImageFilter.GaussianBlur(radius=radius))
    return pygame.image.fromstring(pil_blured.tobytes(), pil_blured.size, pil_blured.mode)
    
def main():
    pygame.init()

    pygame.display.set_caption('Escape Mouse!')
    screen_size = ((CASE_SIZE*len(world[0]), CASE_SIZE*len(world)))
    screen = pygame.display.set_mode(screen_size)
    
    personas = list()
    mouse = Persona('data/mouse_128px.png', get_init_world_position(Item.MOUSE))
    cat = Persona('data/cat_128px.png', get_init_world_position(Item.CAT))
    cat.follow(mouse, [Move.DOWN, Move.DOWN, Move.DOWN])
    goal_pos = get_init_world_position(Item.GOAL)
    personas.append(mouse)
    personas.append(cat)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mouse.move(Move.LEFT)
                if event.key == pygame.K_RIGHT:
                    mouse.move(Move.RIGHT)
                if event.key == pygame.K_UP:
                    mouse.move(Move.UP)
                if event.key == pygame.K_DOWN:
                    mouse.move(Move.DOWN)
        screen.fill((0,0,0))
        for i in range(len(world)):
            for j in range(len(world[i])):
                pygame.draw.rect(screen,
                    world[i][j] & Item.PATH and (255,255,255) or (127,127,127),
                    (j*CASE_SIZE, i*CASE_SIZE, CASE_SIZE, CASE_SIZE), 0)
        pygame.draw.rect(screen,
                    (255,127,0),
                    (goal_pos.x*CASE_SIZE, goal_pos.y*CASE_SIZE, CASE_SIZE, CASE_SIZE), 0)
        for p in personas:
            p.draw(screen)
        if cat.pos == mouse.pos or goal_pos == mouse.pos:
            for radius in range(15):
              screen.blit(blur_surface(screen, radius/4.0), (0,0))
              time.sleep(0.02)
              pygame.display.flip()
            while running:
              for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
        pygame.display.flip()


if __name__=="__main__":
    main()