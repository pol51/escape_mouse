import pygame

CASE_SIZE = 64

WALL = 0
PATH = 1
MOUSE = 2
CAT = 4
GOAL = 8

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
    def __init__(self, img, x=0, y=0):
        sprite = pygame.image.load(img)
        self.sprite = pygame.transform.scale(sprite, (CASE_SIZE, CASE_SIZE))
        self.x = x
        self.y = y
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.x * CASE_SIZE, self.y * CASE_SIZE))
        
    def move_up(self):
        if world[self.y-1][self.x] & PATH:
            self.y -= 1

    def move_down(self):
        if world[self.y+1][self.x] & PATH:
            self.y += 1

    def move_left(self):
        if world[self.y][self.x-1] & PATH:
            self.x -= 1

    def move_right(self):
        if world[self.y][self.x+1] & PATH:
            self.x += 1


def get_init_world_position(flag):
  for i in range(len(world)):
      for j in range(len(world[0])):
          if world[i][j] & flag:
              return (j, i)
        
def main():
    pygame.init()

    pygame.display.set_caption('Escape Mouse!')
    screen = pygame.display.set_mode((CASE_SIZE*len(world[0]), CASE_SIZE*len(world)))
    
    personas = list()
    mouse = Persona('data/mouse_128px.png', *get_init_world_position(MOUSE))
    cat = Persona('data/cat_128px.png', *get_init_world_position(CAT))
    goal_pos = get_init_world_position(GOAL)
    personas.append(mouse)
    personas.append(cat)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mouse.move_left()
                if event.key == pygame.K_RIGHT:
                    mouse.move_right()
                if event.key == pygame.K_UP:
                    mouse.move_up()
                if event.key == pygame.K_DOWN:
                    mouse.move_down()
        screen.fill((0,0,0))
        for i in range(len(world)):
            for j in range(len(world[0])):
                pygame.draw.rect(screen,
                    world[i][j] & PATH and (255,255,255) or (127,127,127),
                    (j*CASE_SIZE, i*CASE_SIZE, CASE_SIZE, CASE_SIZE), 0)
        pygame.draw.rect(screen,
                    (255,127,0),
                    (goal_pos[0]*CASE_SIZE, goal_pos[1]*CASE_SIZE, CASE_SIZE, CASE_SIZE), 0)
        for p in personas:
            p.draw(screen)
        pygame.display.flip()


if __name__=="__main__":
    main()