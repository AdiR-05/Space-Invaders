import pygame


clock = pygame.time.Clock()

class Alien(pygame.sprite.Sprite):
  def __init__(self,type,x,y):
    super().__init__()
    type_of_alien = "invader" + type + ".png"
    self.image = pygame.image.load(type_of_alien).convert_alpha()
    self.image = pygame.transform.scale(self.image,(45,42))
    self.rect = self.image.get_rect(topleft = (x,y))

    if type == "skinny":
      self.value = 30

    elif type == "normal":
      self.value = 20

    else:
      self.value = 10


    

  def update(self,direction_x):
    self.rect.x += direction_x

    

class Extra_alien(pygame.sprite.Sprite):
  def __init__(self,side,display_width):
    super().__init__()
    self.image = pygame.image.load("SuperAlien.png").convert_alpha()
    self.image = pygame.transform.scale(self.image,(60,50))

    if side == "right":
      x = display_width + 50
      self.speed = -3

    else:
      x = -50 
      self.speed = 3
      
    self.rect = self.image.get_rect(topleft = (x,80))

  def update(self):
    self.rect.x += self.speed
