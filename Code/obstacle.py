import pygame 

class Block(pygame.sprite.Sprite):
	def __init__(self,size,color,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft = (x,y))

shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']

#Either have an x or a space.
#Wherever we have an x, we make a block, and if there is a space, nothing happens.
