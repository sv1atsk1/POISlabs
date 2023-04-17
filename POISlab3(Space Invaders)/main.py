import pygame
import random
import os
import time
from pygame import mixer 
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 1100,970
GAME_WINDOW =  pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders")



AQUAMARIN_INVADER = pygame.image.load(os.path.join("assets","aquamarin_enemy.png"))
BLUE_INVADER = pygame.image.load(os.path.join("assets","blue_enemy.png"))
BOLOTNIY_INVADER = pygame.image.load(os.path.join("assets","bolotniy_enemy.png"))
LIGHT_GREEN_INVADER = pygame.image.load(os.path.join("assets","light_green_enemy.png"))
ORANGE_INVADER = pygame.image.load(os.path.join("assets","orange_enemy.png"))
PINK_INVADER = pygame.image.load(os.path.join("assets","pink_enemy.png"))
PURPLE_INVADER = pygame.image.load(os.path.join("assets","purple_enemy.png"))
RED_INVADER = pygame.image.load(os.path.join("assets","red_enemy.png"))
TELECNIY_INVADER = pygame.image.load(os.path.join("assets","telecniy_enemy.png"))
YELLOW_INVADER = pygame.image.load(os.path.join("assets","yellow_enemy.png"))


PLAYER_DEFFENDER = pygame.image.load(os.path.join("assets","player.png"))


YELLOW_LASER = pygame.image.load(os.path.join("assets","yellow_laser.png"))
BOLOTNIY_LASER = pygame.image.load(os.path.join("assets","bolotniy_laser.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","blue_laser.png"))
PLAYER_LASER = pygame.image.load(os.path.join("assets","player_laser.png"))
AQUAMARIN_LASER = pygame.image.load(os.path.join("assets","aquamarin_laser.png"))
LIGHT_GREEN_LASER = pygame.image.load(os.path.join("assets","light_green_laser.png"))
ORANGE_LASER = pygame.image.load(os.path.join("assets","orange_laser.png"))
PINK_LASER = pygame.image.load(os.path.join("assets","pink_laser.png"))
PURPLE_LASER = pygame.image.load(os.path.join("assets","purple_laser.png"))
RED_LASER = pygame.image.load(os.path.join("assets","red_laser.png"))
TELECNIY_LASER = pygame.image.load(os.path.join("assets","telecniy_laser.png"))


BACKGROUND_PICTURE = pygame.transform.scale(pygame.image.load(os.path.join("assets","new_space.jpg")),(WIDTH,HEIGHT))
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets","logo3.png")),(WIDTH,HEIGHT))


SHOOT_SOUND = pygame.mixer.Sound(os.path.join("assets","shoot.wav"))
DEAD_SOUND = pygame.mixer.Sound(os.path.join("assets","enemy-death.wav"))
THEME_SOUND = pygame.mixer.Sound(os.path.join("assets","theme_music.mp3"))
BUTTON_SOUND = pygame.mixer.Sound(os.path.join("assets","button.wav"))


class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move (self,laser_velocity):
        self.y += laser_velocity

    def off_screen(self,height):
        return not (self.y <= height and self.y >=0)

    def collision(self,object):
        return collide(self,object)        

class Entity:
    COOLDOWN = 20

    def __init__(self,x,y,health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.entity_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self,window):
        window.blit(self.entity_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,velocity,object):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(object):
                object.health -= 50
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter +=1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def shootgun_shoot(self):
        if self.cool_down_counter == 0:
            laser1 = Laser(self.x-25,self.y,self.laser_img)
            laser2 = Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser1)
            self.lasers.append(laser2)
            pygame.mixer.Sound.play(SHOOT_SOUND)
            self.cool_down_counter = 1



    def get_width(self):
        return self.entity_img.get_width()
    
    def get_height(self):
        return self.entity_img.get_width()


class Player(Entity):
    def __init__(self,x,y,health = 100):
        super().__init__(x,y,health)
        self.entity_img = PLAYER_DEFFENDER
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.entity_img)
        self.max_health = health
        self.points = 0

    def move_lasers(self,velocity,objects):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for object in objects:
                    if laser.collision(object): 
                        objects.remove(object)
                        pygame.mixer.Sound.play(DEAD_SOUND)
                        self.points += 50
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-25,self.y,self.laser_img)
            self.lasers.append(laser)
            pygame.mixer.Sound.play(SHOOT_SOUND)
            self.cool_down_counter = 1

    def shootgun_shoot(self):
        if self.cool_down_counter == 0:
            laser1 = Laser(self.x-50,self.y,self.laser_img)
            laser2 = Laser(self.x-35,self.y,self.laser_img)
            laser3 = Laser(self.x-20,self.y,self.laser_img)
            laser4 = Laser(self.x-5,self.y,self.laser_img)
            self.lasers.append(laser1)
            self.lasers.append(laser2)
            self.lasers.append(laser3)
            self.lasers.append(laser4)
            pygame.mixer.Sound.play(SHOOT_SOUND)
            self.cool_down_counter = 1


    def draw(self,window):
        super().draw(window)
        self.healthbar(window)


    def healthbar(self,window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.entity_img.get_height() + 10, self.entity_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.entity_img.get_height() + 10, self.entity_img.get_width() * (self.health/self.max_health), 10))

def print_text(message,x,y,font_color = (255,255,255),font_type = "comic.ttf",font_size = 30):
    font_type = pygame.font.Font(font_type,font_size)
    text = font_type.render(message,True,font_color)
    GAME_WINDOW.blit(text,(x,y))

class Enemy(Entity):
    COLOR_MAP = {
                "blue":(BLUE_INVADER,BLUE_LASER),
                "bolotniy":(BOLOTNIY_INVADER,BOLOTNIY_LASER),
                "yellow":(YELLOW_INVADER,YELLOW_LASER),
                "aquamarin":(AQUAMARIN_INVADER,AQUAMARIN_LASER),
                "orange":(ORANGE_INVADER,ORANGE_LASER),
                "pink":(PINK_INVADER,PINK_LASER),
                "purple":(PURPLE_INVADER,PURPLE_LASER),
                "red":(RED_INVADER,RED_LASER),
                "telecniy":(TELECNIY_INVADER,TELECNIY_LASER) 
                }
    
    def __init__(self,x,y,color,health = 100): #"blue","green","yellow"
        super().__init__(x,y,health)
        self.entity_img,self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.entity_img)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-25,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


    def move(self,enemy_velocity):
        self.y += enemy_velocity

def collide(object1,object2):
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask,(offset_x,offset_y)) != None

class Button:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.inactive_clr = (13,162,58)
        self.active_clr = (23,204,58)

    def draw(self,x,y,message,action = None,font_size = 30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(GAME_WINDOW,self.active_clr,(x,y,self.width,self.height))

            if click[0] == 1:
                pygame.mixer.Sound.play(BUTTON_SOUND)
                pygame.time.delay(300)
                if action is not None:
                    action()
        else:
            pygame.draw.rect(GAME_WINDOW,self.inactive_clr,(x,y,self.width,self.height))
        
        print_text(message = message,x = x+10,y = y+10,font_size = font_size)



def main():
    run = True
    FPS = 60
    level = 0
    lives = 1
    player_velocity = 10
    laser_velocity = 20
    enemies = []
    wave_length = 5
    enemy_velocity = 1.5
    lost = False
    lost_count = 0
    points_font = pygame.font.SysFont("comicsans",50)
    main_font = pygame.font.SysFont("comicsans",50)
    #lives_font = pygame.font.SysFont("comicsans",50)
    lost_font = pygame.font.SysFont("comicsans",60)
    player = Player(510,850)
    clock = pygame.time.Clock()

    def window_redraw():
        GAME_WINDOW.blit(BACKGROUND_PICTURE,(0,0))
        
        level_label = main_font.render(f"Level:{level}",1,(255,255,255))
        points_label = points_font.render(f"Points:{player.points}",1,(255,255,255))

        GAME_WINDOW.blit(points_label,(WIDTH/5 - points_label.get_width(),15))
        GAME_WINDOW.blit(level_label,(WIDTH + 20 - points_label.get_width(),15))

        for enemy in enemies:
            enemy.draw(GAME_WINDOW)

        player.draw(GAME_WINDOW)
        
        if lost:
            lost_label = lost_font.render("You Lost!",1,(255,255,255))
            GAME_WINDOW.blit(lost_label,(WIDTH/2 - lost_label.get_width()/2,430))


        pygame.display.update()


    while run:
        clock.tick(FPS)
        window_redraw()

        if lives <=0 or player.health <=0:
            lost = True
            lost_count +=1

        if lost:
            if lost_count > FPS*2:
                run = False
            else: 
                continue

        if len(enemies) == 0:
            level +=1
            wave_length +=5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50,WIDTH-100),random.randrange(-1500,-100),random.choice(["blue","bolotniy","yellow","aquamarin","orange","pink","purple","red","telecniy"])) 
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0:
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH:
            player.x += player_velocity
        if keys[pygame.K_w]  and player.y - player_velocity > 0:
            player.y -= player_velocity
        if keys[pygame.K_s]  and player.y + player_velocity + player.get_height() + 15 < HEIGHT:
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            show_menu()
        if keys[pygame.K_LSHIFT]:
            pause()
        if keys[pygame.K_1]:
            Entity.COOLDOWN = 15
        if keys[pygame.K_2]:
            Entity.COOLDOWN = 5
        if keys[pygame.K_3]:
            Entity.COOLDOWN = 50
            player.shootgun_shoot()
            
            
        

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity,player)
            
            if random.randrange(0,200) == 1:
                enemy.shoot()
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy) 
                pygame.mixer.Sound.play(DEAD_SOUND)
                player.points += 50

            if collide(enemy,player):
                player.health -=50
                enemies.remove(enemy)
                pygame.mixer.Sound.play(DEAD_SOUND)
                player.points += 50

                

            
                 

            
        player.move_lasers(-laser_velocity,enemies)

def show_menu():
    start_button = Button(300,70)
    quit_button = Button(300,70)
    table_of_records_button = Button(300,70)
    pygame.mixer.Sound.stop(THEME_SOUND)
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        GAME_WINDOW.blit(MENU_BACKGROUND,(0,0))
        start_button.draw(400,690,"Start game",game)
        quit_button.draw(400,790,"Quit Game",quit_from_game)
        pygame.display.update()

def quit_from_game():
    quit()               
        
def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pause_font = pygame.font.SysFont("comicsans",55)
        pause_label = pause_font.render("Game on Pause. Press ENTER to continue!",1,(255,255,255))
        GAME_WINDOW.blit(pause_label,(WIDTH/2 - pause_label.get_width()/2,430))
        pygame.mixer.Sound.set_volume(THEME_SOUND,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
                paused = False
                pygame.mixer.Sound.set_volume(THEME_SOUND,100)

        pygame.display.update()


def game():
    title_font = pygame.font.SysFont("comicsans",70)
    run = True
    pygame.mixer.Sound.play(THEME_SOUND)
    while run:
        GAME_WINDOW.blit(BACKGROUND_PICTURE,(0,0))
        title_label = title_font.render("Press the mouse to begin...",1,(255,255,255))
        GAME_WINDOW.blit(title_label,(WIDTH/2 - title_label.get_width()/2,350))
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

show_menu()







