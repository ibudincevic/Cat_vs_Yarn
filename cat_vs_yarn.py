import pygame, sys, random
import time

from pygame.locals import *

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((1200, 622), 0, 32)
pygame.display.set_caption('Cat vs Yarn')
background=pygame.image.load("Super_Mario_mod.png")

WHITE = (255, 255, 255)
ORANGE= (255,  69,   0)
RED   = (255,   0,   0)

no_jump_time=1e15
player_jump_time=no_jump_time
cat_jump_time=no_jump_time
cat_gone_count=no_jump_time

catObj_minus=30  # value used to shrink the hight of the defeated cat rectangle
ground_x=0
ground_y=560
reset_x=50
reset_y=300
jump_frequency=2         # jump duration= FPS/jump_frequency
help_rectangles= False
johnson=True



frames=[]


cat_frames=[]
yarn_frames = []

width=80
height=90
fish_width=40
fish_height=40
player_width=80
player_height=90

yarn_width = fish_width-15
yarn_height = fish_height-15

player_width=width
player_height=height
cat_width=70
cat_height=80

for i in range(1,10):
	cat_frames.append(pygame.transform.scale(pygame.image.load('maca'+'%i'%i+'.png'), (cat_width,cat_height)))
	yarn_frames.append(pygame.transform.scale(pygame.image.load('yarn'+'%i'%i+'.png'), (yarn_width,yarn_height)))

no_maca=pygame.transform.scale(pygame.image.load('maca_yarn.png'), (cat_width-10,cat_height-30))

for i in range(0,9):
	frames.append(pygame.transform.scale(pygame.image.load('frame'+'%i'%i+'_crop.png'), (width,height)))

rest_frame= frames[0]
rest_frame_left=pygame.transform.flip(rest_frame, True, False)

moveRight = False
moveLeft  = False
MOVERATE= 10

player_x = 10
player_y = 300
movement= False

cat_x=400
cat_y=300
reset_cat_x=cat_x
reset_cat_y=cat_y
cat_gone=False   # if True the cat has been hit by the yarn

print_direction= False # for debugging

count=0  # used for counting frames

def terminate():
     pygame.quit()
     sys.exit()

playerObj= { 'surface':pygame.transform.scale(frames[0], (width,height)),
			'facing': 'right',
			'x': player_x,
			'y':player_y,
			'vertical': 'falling',
			'width': player_width,
			'height': player_height
}     

catObj= { 'surface':pygame.transform.scale(cat_frames[0], (width,height)),
			'facing': 'right',
			'x': cat_x,
			'y':cat_y,
			'vertical': 'falling',
			'width': cat_width,
			'height': cat_height,
			'movement': False
}     

class fishObj:
	def __init__(self,image,x,y,width,height,facing,vel):
		self.image = image
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.facing = facing
		self.vel = vel

	def update(self):
		if self.facing == 'left':
			self.x -= self.vel
		elif self.facing == 'right':
			self.x += self.vel
		
class yarnObj:
	def __init__(self,frames,x,y,width,height,facing,vel):
		self.frames = frames
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.facing = facing
		self.vel = vel
	def update(self):
		if self.facing == 'left':
			self.x -= self.vel
		elif self.facing == 'right':
			self.x += self.vel	

fish_group = set([])
yarn_group = set([])
ground=[]

while True: # main loop
	font = pygame.font.Font("freesansbold.ttf", 36)
	text1 = font.render(" Up, Down, Left, Right to move", 1, (10, 10, 10))
	text2 = font.render(""" "d" to fire yarn """, 1, (10, 10, 10))
	text3 = font.render(""" "r" to reset """, 1, (10, 10, 10))
	text4 = font.render(""" "ESC" to quit """, 1, (10, 10, 10))

	background.blit(text1, (0,10))
	background.blit(text2, (0,40))
	background.blit(text3, (0,70))
	background.blit(text4, (0,100))
	DISPLAYSURF.fill(WHITE)
	DISPLAYSURF.blit(background,(0,0))
	count+=1

	if help_rectangles== True:

		pygame.draw.rect(DISPLAYSURF, RED, (ground_x, ground_y, 95, 90))
		pygame.draw.rect(DISPLAYSURF, RED, (ground_x+197, ground_y, 1200, 90))
		pygame.draw.rect(DISPLAYSURF, RED, (playerObj['x']+playerObj['width']/4,playerObj['y'],playerObj['width']/2,playerObj['height']))
		if cat_gone==False:		
			pygame.draw.rect(DISPLAYSURF, ORANGE, (catObj['x']+cat_width/8,catObj['y'],catObj['width'],catObj['height']))
		else:
			pygame.draw.rect(DISPLAYSURF, ORANGE, (catObj['x']+cat_width/8,catObj['y']+catObj_minus,catObj['width'],catObj['height']))
		
		for fish in fish_group:
			pygame.draw.rect(DISPLAYSURF, ORANGE, (fish.x,fish.y,fish.width,fish.height))

	
	ground.append(pygame.Rect(ground_x,ground_y,95,90))
	ground.append(pygame.Rect(ground_x+197,ground_y,1200,90))		
	
		
	playerObj['rect']=pygame.Rect(playerObj['x']+playerObj['width']/4,playerObj['y'],playerObj['width']/2,playerObj['height']-10)

	if cat_gone==False:
		catObj['rect'] = pygame.Rect(catObj['x']+cat_width/8,catObj['y'],catObj['width'],catObj['height']+10)
		ground_cat = pygame.Rect(catObj['x']+cat_width/8,catObj['y'],catObj['width'],catObj['height'])
	else:
		catObj['rect'] = pygame.Rect(catObj['x']+cat_width/8,catObj['y']+catObj_minus,catObj['width'],catObj['height'])
		ground_cat = pygame.Rect(catObj['x']+cat_width/8,catObj['y']+catObj_minus,catObj['width'],catObj['height'])
	

	# check if  the player collided with the ground or landed on the cat
	for i in ground:	
		if playerObj['rect'].colliderect(i):						
			playerObj['vertical']='still'
			break
		elif playerObj['rect'].colliderect(ground_cat):
			playerObj['vertical']='still'
			break						
		elif count - player_jump_time >= FPS/jump_frequency or player_jump_time==no_jump_time:		
			playerObj['vertical']='falling'		

	# check if player hit the fish
	for fish in fish_group:
		if playerObj['rect'].colliderect(pygame.Rect(fish.x,fish.y,fish.width,fish.height)):
			if count %2 == 0:
				DISPLAYSURF.blit(pygame.image.load('game_over.png'), (200+random.randint(0,500),100+random.randint(0,300)))
				DISPLAYSURF.blit(pygame.image.load('game_over.png'), (700+random.randint(0,500),100+random.randint(0,300)))
				DISPLAYSURF.blit(pygame.image.load('game_over.png'), (0+random.randint(0,500),100+random.randint(0,300)))
				DISPLAYSURF.blit(pygame.image.load('game_over.png'), (600+random.randint(0,500),100+random.randint(0,300)))
				DISPLAYSURF.blit(pygame.image.load('game_over.png'), (100+random.randint(0,500),100+random.randint(0,300)))
				DISPLAYSURF.blit(pygame.image.load('game_over.png'), (400+random.randint(0,500),100+random.randint(0,300)))
				DISPLAYSURF.blit(pygame.image.load('game_over.png'), (500+random.randint(0,500),100+random.randint(0,300)))								

	# check if yarn hit the cat
	for yarn in set(yarn_group):
		if 	pygame.Rect(yarn.x,yarn.y,yarn.width,yarn.height).colliderect(catObj['rect']) and cat_gone==False:
			cat_gone = True
			cat_gone_count=count
			yarn_group.remove(yarn)
			if johnson==True:
				pygame.mixer.music.load('long_johnson.mp3')
				pygame.mixer.music.play(0, 0.5)	
		
	# check if the cat collided with the ground
	for i in ground:	
		if catObj['rect'].colliderect(i):						
			catObj['vertical']='still'
			break
		elif count - cat_jump_time >= FPS/jump_frequency or cat_jump_time==no_jump_time:		
			catObj['vertical']='falling'	
				
	# check if player and cat are falling
	if count - player_jump_time >= FPS/jump_frequency:
		player_jump_time= no_jump_time
		playerObj['vertical']= 'falling'
		
	if count - cat_jump_time >= FPS/jump_frequency:
		cat_jump_time= no_jump_time
		catObj['vertical']= 'falling'		

	if playerObj['vertical']=='falling':
		playerObj['y'] += MOVERATE	
	if catObj['vertical']=='falling':
		catObj['y'] += MOVERATE	

	# cat jump/fire fish
	if count%40==0:
		rand_int = random.randint(0,100)		
		if rand_int>30:						
			if cat_gone==False:
				
				if catObj['x']>playerObj['x']:										
					fish_group.add(fishObj(pygame.transform.scale(pygame.image.load('fishy.png'), (fish_width,fish_height)),catObj['x']-catObj['width']/2,catObj['y'],fish_width,fish_height,'left',random.randint(5,10)))

				elif catObj['x']< playerObj['x']:					
					fish_group.add(fishObj(pygame.transform.scale(pygame.image.load('fishy.png'), (fish_width,fish_height)),catObj['x']+catObj['width']/2,catObj['y'],fish_width,fish_height,'right',random.randint(5,10)))
				cat_jump_time=count
			

	# delete off-screen fish			
	for fish in set(fish_group):
		if fish.x > -40 and fish.x < 1220:
			fish.update()
		else:
			fish_group.remove(fish)
	
	# delete off-screen yarn		
	for yarn in set(yarn_group):
		if yarn.x > -40 and yarn.x < 1220:
			yarn.update()
		else:
			yarn_group.remove(yarn)

	
	for event in pygame.event.get():

		if event.type==QUIT:
			terminate()
		elif event.type==KEYDOWN:
						
			if event.key == K_r:				
				playerObj['x']=reset_x
				playerObj['y']=reset_y
				playerObj['vertical']='falling'
				catObj['x']=reset_cat_x
				catObj['y']=reset_cat_y
				cat_gone=False

			if event.key == K_d:
				yarn_group.add(yarnObj(yarn_frames,playerObj['x']+playerObj['width']/2,playerObj['y']+playerObj['height']/4,yarn_width,yarn_height,playerObj['facing'],8))

			if event.key == K_UP:				
				if playerObj['vertical']=='still':
					playerObj['vertical']='jump'
					player_jump_time=count

			elif event.key == K_DOWN:				
				if print_direction==True:
					print "down"
				
			elif event.key == K_RIGHT:				
				playerObj['facing']='right'
				moveRight= True
				moveLeft= False
				rest_frame=frames[0]
				if print_direction==True:
					print "right"
				movement= True
				
			elif event.key == K_LEFT:				
				playerObj['facing']= 'left'
				moveLeft= True				
				moveRight= False
				movement= True
				if print_direction==True:
					print "left"		
				
		elif event.type == KEYUP:

			if event.key == K_LEFT:
				if print_direction==True:
					print "leftup"				
				moveLeft  = False
				if moveRight == False:
					movement= False

			elif event.key == K_RIGHT:
				moveRight = False
				if print_direction==True:
					print "rightup"				
				if moveLeft == False:
					movement= False

			elif event.key == K_UP:				
				if print_direction==True:			
					print "up up"

			elif event.key == K_DOWN:				
				if print_direction==True:
					print "down up"

			elif event.key == K_ESCAPE:
				terminate()
				
	# move the player/cat			
	if moveLeft:		
		playerObj['x'] -= MOVERATE		
	if moveRight:
		playerObj['x'] += MOVERATE		
	
	if player_jump_time!=no_jump_time:
		playerObj['y'] -= MOVERATE          
	
	if cat_jump_time!= no_jump_time:		
		catObj['y']    -= MOVERATE

	if count - cat_gone_count > 72:
		pygame.mixer.music.stop()

	# draw objects on screen -------------------------------------------------------------------------------------------------------------	

	# player drawing
	if movement == False:		
		if playerObj['facing']== 'right':			
			DISPLAYSURF.blit(rest_frame, (playerObj['x'],playerObj['y']))
		elif playerObj['facing'] == 'left':
			DISPLAYSURF.blit(rest_frame_left, (playerObj['x'],playerObj['y']))		
	else:	
		if playerObj['facing']== 'right':			
			DISPLAYSURF.blit(frames[(count/3)%8], (playerObj['x'],playerObj['y']))			
		elif playerObj['facing'] == 'left':
			DISPLAYSURF.blit(pygame.transform.flip(frames[(count/3)%8], True, False), (playerObj['x'],playerObj['y']))				

	# cat drawing
	if cat_gone==False:
		if catObj['movement']== False:
			DISPLAYSURF.blit(cat_frames[1], (catObj['x'],catObj['y']))
	else:
		DISPLAYSURF.blit(no_maca, (catObj['x'],catObj['y']+catObj_minus))		
	# cat drawing

	# fish drawing
	for fish in fish_group:
		if fish.facing == 'left':
			DISPLAYSURF.blit(fish.image, (fish.x,fish.y))
		elif fish.facing == 'right':
			DISPLAYSURF.blit(pygame.transform.flip(fish.image, True, False), (fish.x,fish.y))							
	# fish drawing

	# yarn drawing	
	for yarn in yarn_group:
		DISPLAYSURF.blit(yarn.frames[(count/2)%9], (yarn.x,yarn.y))
	# yarn drawing

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()
	fpsClock.tick(FPS)					

