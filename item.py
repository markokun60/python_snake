import pygame
import os
import math
import constants

class Item():
	SCALE_VALUE = 0.15
	SCALE_BASE  = 1 - SCALE_VALUE
	def __init__(self,img,r,c):
		self.row = r
		self.col = c
		self.image_orig  = img
		self.image       = self.image_orig.copy()
		#self.scaled_rect = self.image.get_rect(
		#	center = (self.col * CELL_SIZE + CELL_SIZE / 2, self.row * CELL_SIZE + CELL_SIZE / 2))

	def draw(self,screen):
		scale =  self.SCALE_BASE +  math.sin(pygame.time.get_ticks() / 600) * self.SCALE_VALUE
		self.image = pygame.transform.smoothscale_by(self.image_orig, scale)
		#self.scaled_rect = self.image.get_rect(
		#	center = (self.col * CELL_SIZE + CELL_SIZE / 2, self.row * CELL_SIZE + CELL_SIZE / 2))
		
		#screen.blit(self.image, self.scaled_rect)

		y = constants.row_to_y(self.row)
		y += (constants.CELL_SIZE - self.image.get_height()) //2

		x  = constants.col_to_x(self.col) 
		x += (constants.CELL_SIZE - self.image.get_width()) //2
		
		screen.blit(self.image, (x,y))
   




