import pygame
from laser import Laser
from replit import audio

class Player(pygame.sprite.Sprite):
  def __init__(self,pos,constraint,speed):
    super().__init__()
    self.image = pygame.image.load("player.png").convert_alpha()
    self.rect = self.image.get_rect(midbottom = pos)
    self.speed = speed
    self.max_x_constraint = constraint
    self.ready = True
    self.laser_time = 0
    self.laser_cooldown = 600 # 600 ms
    self.lasers = pygame.sprite.Group()

  def get_input(self):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT]:
      self.rect.x += self.speed
    if keys[pygame.K_LEFT]:
      self.rect.x -= self.speed
    if keys[pygame.K_SPACE] and self.ready:
      self.shoot_laser()
      laser_source = audio.play_file("audio_laser.wav")
      self.ready = False
      self.laser_time = pygame.time.get_ticks()

  def recharge(self):
    if not self.ready: #checks if self.ready is false
      current_time = pygame.time.get_ticks()
      if current_time - self.laser_time >= self.laser_cooldown:
        self.ready = True
      
  

  
  def constraint(self):
    if self.rect.left <0: 
      self.rect.left = 0
    if self.rect.right >self.max_x_constraint: 
      self.rect.right = self.max_x_constraint
  
  def shoot_laser(self):
    self.lasers.add(Laser(self.rect.center,-15,self.rect.bottom,"Green"))
    
    

  
  def update(self):
    self.get_input()
    self.constraint()
    self.recharge()
    self.lasers.update()
