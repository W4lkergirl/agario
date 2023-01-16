import pygame
from pygame.locals import *
from sys import exit
from random import randint 
import math

pygame.init()

som_comer = pygame.mixer.Sound('comer.wav')
som_morrer = pygame.mixer.Sound('morrer.wav')
som_comerfood = pygame.mixer.Sound('comerfood.wav')

morreu = False

WIDTH = 1000
HEIGHT = 600
x = WIDTH/2 - 25
y = HEIGHT/2 - 20

def randRGB():
	r = randint(0,255)
	g = randint(0,255)
	b = randint(0,255)
	return (r, g, b)

def exibeMensagem(msg, tamanho, cor):
	fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
	mensagem = f'{msg}'
	texto_formatado = fonte.render(mensagem, True, cor)
	return texto_formatado

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WALKERS")
clock = pygame.time.Clock()

############################## ENTIDADES  ##################################
class Circle(object):

	def __init__(self, x, y, radius, color):
		self.x = x 
		self.y = y 
		self.radius = radius 
		self.color = color

	def show(self):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

	def distCenterSquare(self, circle):
		return (self.x-circle.x)**2+(self.y-circle.y)**2

	def collide(self, circle):
		if self.distCenterSquare(circle) <= (self.radius+circle.radius)**2:
			return True 
		return False

class Food(Circle):
	def __init__(self):
		super().__init__(randint(0,WIDTH), randint(0,HEIGHT), 2,randRGB())

class Player(Circle):
	def __init__(self, x, y, radius, color):
		if radius == -1:
			radius = randint(15,20)
		if color == -1: 
			color = randRGB()
		super().__init__(x, y, radius, color)

	def somethingInside(self, something):
		if self.distCenterSquare(something) < self.radius**2:
			return True
		return False

	def moveRight(self):
		if self.x + 100*1/self.radius < WIDTH:
			self.x = self.x + 100*1/self.radius
	
	def moveLeft(self):
		if self.x - 100*1/self.radius > 0:
			self.x = self.x - 100*1/self.radius

	def moveUp(self):
		if self.y - 100*1/self.radius > 0:
			self.y = self.y - 100*1/self.radius
	
	def moveDown(self):
		if self.y + 100*1/self.radius < HEIGHT:
			self.y = self.y + 100*1/self.radius	

class Bot(Player):

	def __init__(self):
			x = randint(0,WIDTH)
			y = randint(0,HEIGHT)
			radius = randint(4,15)
			color = randRGB()
			super().__init__(x, y, radius, color)

	def fujir(self, player):
		if(self.distCenterSquare(player) < 150**2):
			if player.x <= self.x:
				self.moveRight()
			if player.x > self.x:
				self.moveLeft()
			if player.y <= self.y:
				self.moveDown()
			if player.y < self.y:
				self.moveUp()

	def unir(self, bot):
		if(self.distCenterSquare(bot) < 100**2):
			if bot.x <= self.x:
				self.moveLeft()
			if bot.x > self.x:
				self.moveRight()
			if bot.y <= self.y:
				self.moveUp()
			if bot.y > self.y:
				self.moveDown()

	def walk(self):
		rand = randint(0,3)
		if rand == 0:
			self.moveUp()
		elif rand == 1:
			self.moveDown()
		elif rand == 2:
			self.moveLeft()
		else:
			self.moveRight()
############################## LISTAS DE ENTIDADES  ##################################

foodlist = list()
for i in range(1000):
	foodlist.append(Food())

player = Player(40, 50, -1, -1)

botList = list()
for i in range(10):
	botList.append(Bot())

while True:
	clock.tick(30)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()

	if morreu == False:
		screen.fill((0,0,0))
		for food in foodlist:
			if player.somethingInside(food):
				player.radius = math.sqrt(player.radius**2 + food.radius**2)
				foodlist.remove(food)
				foodlist.append(Food())
				som_comerfood.play()

		for bot in botList:
			if bot.radius > player.radius:
				bot.unir(player)
			else:
				bot.fujir(player)
			bot.walk()
			if player.somethingInside(bot) and player.radius > bot.radius:
				player.radius = math.sqrt(player.radius**2 + bot.radius**2)
				botList.remove(bot)
				botList.append(Bot())
				som_comer.play()
			for food in foodlist:
				if bot.somethingInside(food):
					bot.radius = math.sqrt(bot.radius**2 + food.radius**2)
					foodlist.remove(food)
					foodlist.append(Food())
			for bot2 in botList:
				if bot2 != bot:
					bot.unir(bot2)
					if bot.somethingInside(bot2):
						if(bot.radius > bot2.radius):
							bot.radius = math.sqrt(bot.radius**2 + bot2.radius**2)
							botList.remove(bot2)
							botList.append(Bot())
					if bot.somethingInside(player) and bot.radius > player.radius:
						player.radius = 0.1
						som_morrer.play()
						game_over = exibeMensagem('GAME OVER', 100, (255,0,0))
						screen.blit(game_over,(265,250))
						morreu = True

		for food in foodlist:
			food.show()

		for bot in botList:
			bot.show()

		player.show()

		if pygame.key.get_pressed()[K_a]:
			player.moveLeft()
		if pygame.key.get_pressed()[K_d]:
			player.moveRight()
		if pygame.key.get_pressed()[K_w]:
			player.moveUp()
		if pygame.key.get_pressed()[K_s]:	
			player.moveDown()

	pygame.display.update()