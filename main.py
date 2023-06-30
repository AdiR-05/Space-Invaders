from __future__ import absolute_import, division, print_function
import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra_alien
from random import choice,randint
from replit import audio
from laser import Laser
import time
from itertools import cycle

class Game:
  def __init__(self): #Add sprite groups in here 
    #Player setup
    playerSprite = Player((display_width/2,display_height),display_width,5) 
    self.player = pygame.sprite.GroupSingle(playerSprite)

    #Obstacles setup
    self.shape = obstacle.shape
    self.block_size = 6
    self.blocks = pygame.sprite.Group()
    self.create_multiple_obstacles((0,150,300,450), x_start =  display_width/15, y_start = 480)


    #Alien setup
    self.aliens = pygame.sprite.Group()
    self.alien_lasers = pygame.sprite.Group()
    
    self.alien_maker(rows = 11,cols = 5)
    self.alien_direction_y = 0
    self.alien_direction_x = 1

    self.extra = pygame.sprite.GroupSingle()
    self.extra_spawn_time = randint(400,800)

    #Health setup
    self.lives = 3
    self.lives_surf = pygame.image.load("player.png").convert_alpha()
    self.lives_surf = pygame.transform.scale(self.lives_surf,(30,30))
    self.lives_x_start = display_width - (self.lives_surf.get_size()[0] * 3 + 20)


    #score setup
    self.score = 0
    self.font = pygame.font.Font("space_invaders.ttf",20)

      
    

  def create_obstacle(self, x_start, y_start,offset_x):
    for row_index, row in enumerate(self.shape):
      for col_index,col in enumerate(row):
        if col == 'x':
          x = x_start + col_index * self.block_size + offset_x
          y = y_start + row_index * self.block_size
          block = obstacle.Block(self.block_size,("Green"),x,y)
          self.blocks.add(block)

  
  def create_multiple_obstacles(self,offset,x_start,y_start):
    for offset_x in offset:
      self.create_obstacle(x_start,y_start,offset_x)
      
    
  
  def alien_maker(self,rows,cols,x_distance = 45,y_distance = 45,x_offset = 50, y_offset = 120):
    for row_index, row in enumerate(range(rows)):
      for col_index, col in enumerate(range(cols)):
        x = row_index * x_distance + x_offset
        y = col_index * y_distance + y_offset
        
        if col_index == 0: 
          alien_sprite = Alien('skinny',x,y)
        elif col_index == 1 or col_index == 2: 
          alien_sprite = Alien('normal',x,y)
        else: 
          alien_sprite = Alien('fat',x,y)
				
        self.aliens.add(alien_sprite)


  
  def alien_pos_checker(self):
    all_aliens = self.aliens.sprites()
    for alien in all_aliens:
      if alien.rect.right >= 600:
        self.alien_direction_x = -1
        self.alien_move_down(2)

      

      elif alien.rect.left <=0:
        self.alien_direction_x = 1
        self.alien_move_down(2)

  
  def alien_move_down(self,distance):
    if self.aliens:
      for alien in self.aliens.sprites():
        alien.rect.y += distance

  
  def alien_shoot(self):
    if self.aliens.sprites():
      random_alien = choice(self.aliens.sprites())
      laser_sprite = Laser(random_alien.rect.center,6,display_height,"white")
      self.alien_lasers.add(laser_sprite)
      
    
  
  def extra_alien_timer(self):
    self.extra_spawn_time -= 1
    if self.extra_spawn_time <= 0:
      self.extra.add(Extra_alien(choice(["right","right"]),display_width))
     
      self.extra_spawn_time = randint(400,800)



  def collision_checker(self):

    #player lasers
    if self.player.sprite.lasers:
      for player_laser in self.player.sprite.lasers:
        
        #Obstacle collision with player laser
        if pygame.sprite.spritecollide(player_laser,self.blocks,True):
          player_laser.kill()
        #Alien collision with player laser
        aliens_hit = pygame.sprite.spritecollide(player_laser,self.aliens,True)
        if aliens_hit:
          for alien in aliens_hit:
            self.score += alien.value
 
          player_laser.kill()
          
            
        # Extra collision with player laser
        if pygame.sprite.spritecollide(player_laser,self.extra,True):
          player_laser.kill()
          self.score += randint(30,50)
          

    if self.alien_lasers:
      for laser in self.alien_lasers:
        #Alien laser hits obstacle
        if pygame.sprite.spritecollide(laser,self.blocks,True):
          laser.kill()

        #Alien laser hits player
        if pygame.sprite.spritecollide(laser,self.player,False):
          laser.kill()
          self.lives -= 1
          explosion_source = audio.play_file("audio_explosion.wav")
          if self.lives<=0:
            crash()



    if self.aliens:
      for alien in self.aliens: #if aliens collide with blocks, it kills the blocks
        pygame.sprite.spritecollide(alien,self.blocks,True)

        #if aliens collide with player, game over and we call the crash function
        if pygame.sprite.spritecollide(alien,self.player,True):
          crash()


  
  
  def display_lives(self):
    for live in range(self.lives):
      x = self.lives_x_start + (live*35)
      screen.blit(self.lives_surf,(x,8))

  def display_score(self):
    score_surf = self.font.render(f"Score: {self.score}",False,"White")
    score_rect = score_surf.get_rect(topleft = (0,0))
    screen.blit(score_surf,score_rect)
  
  
  def victory_message(self):
    if not self.aliens.sprites():
      victory_surf = self.font.render("You won",False,"white")
      victory_rect = victory_surf.get_rect(center=(display_width/2, display_height/2))
      screen.blit(victory_surf,victory_rect)
      pygame.display.update()
      quitgame()
      

      
  def run(self): #Update all sprite groups and draw all of them.
    self.player.update()
    self.alien_lasers.update()
    self.aliens.update(self.alien_direction_x)
    self.alien_pos_checker()
    self.player.draw(screen)
    self.player.sprite.lasers.draw(screen)
    self.collision_checker()


    self.extra_alien_timer()
    self.extra.update()
    
    self.blocks.draw(screen)

    self.aliens.draw(screen)
    self.alien_lasers.draw(screen)
    self.extra.draw(screen)
    self.display_lives()
    self.display_score()
    self.victory_message()
    







def text_objects(text, font,colour): #Function used to display our text and takes parameters of the text, the font and its colour.
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def fast_quit():
  pygame.quit()
  quit()

def quitgame():
  time.sleep(4)
  pygame.quit()
  quit()

def button_maker(msg,x,y,width,height,col,hover_col,action = None): # col = colour of box, hover_col = colour of text when we hover over it.
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()

  smallText = pygame.font.Font("space_invaders.ttf",20)
  
  if x+width > mouse[0] > x and y+height>mouse[1] > y:
    textSurf, textRect = text_objects(msg, smallText,hover_col)
    pygame.draw.rect(screen,col,(x,y,width,height))
    textRect.center = ( (x+(width/2)), (y+(height/2)) )
    screen.blit(textSurf, textRect)
  
    
    
    if click[0] == 1 and action == "gamestart":
      return "start"
    elif click[0] == 1 and action == "fast_quit":
      fast_quit()
      
  else: 
    textSurf, textRect = text_objects(msg, smallText,"White")
    pygame.draw.rect(screen,col,(x,y,width,height))
    textRect.center = ( (x+(width/2)), (y+(height/2)) )
    screen.blit(textSurf, textRect)

def crash():  # Here we display a message when we crash
    largeText = pygame.font.Font("space_invaders.ttf",50)
    

    screen.fill((10,10,10))
    TextSurf, TextRect = text_objects("GAME OVER", largeText,"green")
    TextRect.center = ((display_width/2),(display_height/2))
    screen.blit(TextSurf, TextRect) 
      
    pygame.display.update()  
    quitgame()
    
    


def game_intro():
    intro = True
    title_surf = pygame.image.load("titleSi.png")
    title_surf = pygame.transform.scale(title_surf,(300,150))
    title_rect = title_surf.get_rect(center = (display_width/2,75))

    scoretable = pygame.image.load("scoretable.png")
    scoretable = pygame.transform.scale(scoretable, (400, 350))
    scoretable_rect = scoretable.get_rect(center = (display_width/2,520))

    smallText = pygame.font.Font("space_invaders.ttf",20)
    adi_surf = smallText.render("By Adi Ranjan",True,"White")
    adi_rect = adi_surf.get_rect(midbottom = (300,600))

    
    while intro:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()

      screen.fill("Black")
      screen.blit(title_surf,title_rect)
      screen.blit(scoretable,scoretable_rect)
      screen.blit(adi_surf,adi_rect)

      status = button_maker("START",200,180,200,50,"Black","Green","gamestart")
      if status == "start":
        break
      button_maker("QUIT",200,280,200,50,"Black","Green","fast_quit")
      
      pygame.display.update()
      clock.tick(15)


def rules():
  smallText = pygame.font.Font("space_invaders.ttf",20)
  textFont = pygame.font.Font("space_invaders.ttf",50)
  keyboard_surf = pygame.image.load("keyboard(1).png").convert_alpha()
  keyboard_surf = pygame.transform.scale(keyboard_surf,(550,450))
  keyboard_rect = keyboard_surf.get_rect(center = (300,300))
  
  

  BLINK_EVENT = pygame.USEREVENT + 0
  
  on_text_surf = textFont.render("Spacebar to shoot",False,"White")
  blink_rect = on_text_surf.get_rect(center = (300,100))
  off_text_surface = pygame.Surface(blink_rect.size)
  blink_surfaces = cycle([on_text_surf, off_text_surface])
  blink_surface = next(blink_surfaces)
  pygame.time.set_timer(BLINK_EVENT, 600)

  on_text_surf2 = textFont.render("Arrows to move",False,"White")
  blink_rect2 = on_text_surf2.get_rect(center = (300,170))
  off_text_surface2 = pygame.Surface(blink_rect2.size)
  blink_surfaces2 = cycle([on_text_surf2, off_text_surface2])
  blink_surface2 = next(blink_surfaces2)
  pygame.time.set_timer(BLINK_EVENT, 600)
  static_time = pygame.time.get_ticks()

  
  while True:

      
      running_time = pygame.time.get_ticks()
      timer = running_time - static_time
      remaining_time = 10000 - timer 
      gametime_surf = smallText.render(f"Game starting in: {remaining_time/1000}",False,"White")
      gametime_rect = gametime_surf.get_rect(center = (300,450))
      


      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()

        if event.type == BLINK_EVENT:
          blink_surface = next(blink_surfaces)
          blink_surface2 = next(blink_surfaces2)
      
      
      screen.fill("Black")
      screen.blit(keyboard_surf,keyboard_rect)
      whiteblock = pygame.draw.rect(screen,"White",pygame.Rect(218,345,147,16))
      block = pygame.draw.rect(screen,"White",pygame.Rect(370,344,19,16))
      block2 = pygame.draw.rect(screen,"White",pygame.Rect(419,344,19,16))

      
    
      screen.blit(gametime_surf,gametime_rect)
    
      screen.blit(blink_surface,blink_rect)

      screen.blit(blink_surface2,blink_rect2)

      if remaining_time < 0:
        break
      
      pygame.display.update()
      clock.tick(15)

        
def game_loop():
  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == ALIENLASER:
          game.alien_shoot()
    
  
    screen.fill((10,10,10))
    game.run()
    

    pygame.display.update()
    clock.tick(60)







if __name__ == "__main__": #If statement prevents running files we don't want to run
  pygame.init()

  display_width = 600
  display_height = 600
  screen = pygame.display.set_mode((display_width, display_height))
  clock = pygame.time.Clock()
  pygame.display.set_caption("Space invaders")
  game = Game()

  
  ALIENLASER = pygame.USEREVENT + 1
  pygame.time.set_timer(ALIENLASER,800)

  game_intro()
  rules()
  game_loop()
