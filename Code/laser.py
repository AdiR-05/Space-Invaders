import pygame

class Laser(pygame.sprite.Sprite):
  def __init__(self,pos,speed,display_height,colour):
    super().__init__()
    self.image = pygame.Surface((4,20))
    self.image.fill(colour)
    self.rect = self.image.get_rect(center = pos)
    self.speed = speed
    self.max_y_constraint = display_height
    


  def destroy(self):
    if self.rect.y <=-50 or self.rect.y >= self.max_y_constraint+50 :
      self.kill()

    
  def update(self):
    self.rect.y += self.speed
    self.destroy()
