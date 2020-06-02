import pygame as pg, os, time, random
pg.font.init()

#Initialize Window
WIDTH, HEIGHT = 750, 750
WIN = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Space Shooter")
#window has x,y coordinates x increase go to right y increase go down

#Load images from assets
#Enemy ships
RED_SPACE_SHIP = pg.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pg.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pg.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
#Player ship
YELLOW_SPACE_SHIP = pg.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
#Lasers
RED_LASER = pg.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pg.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pg.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pg.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
#Background
BG = pg.image.load(os.path.join("assets", "background-black.png"))
#scale the background to the window size
BG = pg.transform.scale(BG,(WIDTH,HEIGHT))

class Ship:
    COOLDOWN = 30 #wait 30 frames or .5secs to shoot another laser

    def __init__(self,x,y,health = 100):
        self.x, self.y = x, y #starting position of the ship
        self.health = health #current health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_count = 0 #wait for a certain amount of time to fire a laser again
    
    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:   laser.draw(window)

    def get_width(self):    return self.ship_img.get_width()
    def get_height(self):    return self.ship_img.get_height()

    def cooldown(self): #handles the cooldown period
        if self.cooldown_count >= self.COOLDOWN: #if the cooldown has finished reset it to 0
            self.cooldown_count = 0
        elif self.cooldown_count > 0:   #otherwise increment the counter until it does reach the limit
            self.cooldown_count += 1

    def shoot(self):
        if self.cooldown_count == 0: #make sure the cooldown to shoot anoter laser is finished
            laser = Laser(self.x,self.y,self.laser_img) #make a laser
            self.lasers.append(laser) #add to the list
            self.cooldown_count = 1 #set the cooldown counter
    
    def move_lasers(self,vel,o):
        self.cooldown() #increment the cooldown while lasers are moving
        for laser in self.lasers:
            laser.move(vel) #move the lasers
            if laser.off_screen(HEIGHT): #if the laser is off screen
                self.lasers.remove(laser)
            elif laser.collision(o): #if an enemy laser hit the player
                o.health -= 10
                self.lasers.remove(laser)



class PlayerShip(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        #make a mask that tells where the pixels are and aren't from the image to check collision
        self.mask = pg.mask.from_surface(self.ship_img)
        self.max_health = health #starting health

    def move_lasers(self, vel, o):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel) #move the lasers
            if laser.off_screen(HEIGHT): #if the laser is off screen
                self.lasers.remove(laser)
            else:
                for obj in o:
                    if laser.collision(obj): #if an player laser hit the enemy
                        o.remove(obj) #remove the enemy and the laser
                        if laser in self.lasers:    self.lasers.remove(laser)
                        return True
        return False

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    def healthbar(self,window): #made of 1 red and 1 green rectangle to show current health right below the player
        pg.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, 
        self.ship_img.get_width(), 10))
        pg.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, 
        self.ship_img.get_width() * (self.health/self.max_health), 10))


class EnemyShip(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }
    def __init__(self, x, y, color,health=100):
        super().__init__(x, y, health=health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pg.mask.from_surface(self.ship_img)
    
    def move(self,vel):
        self.y += vel

    def shoot(self):
        if self.cooldown_count == 0: 
            laser = Laser(self.x - 17,self.y,self.laser_img) #position the laser at the center of ship
            self.lasers.append(laser) 
            self.cooldown_count = 1

class Laser:
    def __init__(self,x,y,img):
        self.x, self.y = x, y
        self.img = img
        self.mask = pg.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y)) 
    
    def move(self,vel):
        self.y += vel
    
    def off_screen(self,height):    return not (self.y <= HEIGHT and self.y >= 0)

    def collision(self,obj):    return collide(self,obj) #see if a laser collided with an object
        
def collide(o1, o2):
    offx = o2.x - o1.x
    offy = o2.y - o1.y
    #see if the 2 objects' masks overlap based on the difference of their top left coordinates
    return o1.mask.overlap(o2.mask, (offx, offy)) is not None #return point of intersection if not none

def main():
    run = True
    #frame rate
    fps = 60
    clock = pg.time.Clock()
    
    player_vel = 5 #how many pixels you can move with each button press
    laser_vel = 10
    
    level, score, lives = 0,0, 5
    
    enemies = []
    enemy_vel = 1
    wave_length = 5
    
    main_font = pg.font.SysFont("comicsans", 40) #font used for text
    
    lost_font = pg.font.SysFont("comicsans", 50)
    lost = False
    lost_count = 0
    
    player = PlayerShip(325,600)
    
    def redraw_win():
        #redraw the background at the top left of the screen, basically at its original position
        WIN.blit(BG,(0,0))
        #put the lives and level as text on the window
        #create the labels
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        score_label = main_font.render(f"Score: {score}", 1, (255,255,255))
        #position the labels at these coordinates
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, ((WIDTH - score_label.get_width())/2, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)

        if lost: #display game over text
            lost_label = lost_font.render("Game Over",1,(255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        pg.display.update()

    while run:
        #set frame rate
        clock.tick(fps)
        redraw_win()
        #game over conditions
        if lives < 1 or player.health < 1:  
            lost = True
            lost_count += 1

        if lost: #if the game over message is on for over 5 seconds stop the game
            if lost_count > fps*5:  run = False
            else:   continue

        #if there are no more enemies then go to next level
        if len(enemies) == 0:   
            level += 1
            #restore 20% health when level complete
            if player.health < 80:  player.health += 20
            else:   player.health = 100
            wave_length += 5
            for i in range(wave_length):
                enemy = EnemyShip(random.randrange(50, WIDTH - 100),random.randrange(-1500,-100),
                random.choice(["red","blue","green"]))
                enemies.append(enemy)

        for event in pg.event.get(): #Loop through all events
            #If someone wants to exit the game then quit the loop
            if event.type == pg.QUIT:   quit()
        keys = pg.key.get_pressed() #tells which keys are being pressed at the moment
        #move the ship based on input and make sure it stays within the bounds of the window
        if (keys[pg.K_a] or keys[pg.K_LEFT]) and player.x - player_vel > 0:   player.x -= player_vel
        if (keys[pg.K_d] or keys[pg.K_RIGHT]) and player.x + player_vel + player.get_width() < WIDTH:   player.x += player_vel
        if (keys[pg.K_w] or keys[pg.K_UP]) and player.y - player_vel > 25:   player.y -= player_vel
        if (keys[pg.K_s] or keys[pg.K_DOWN]) and player.y + player_vel + player.get_height() + 15 < HEIGHT:   player.y += player_vel
        if keys[pg.K_SPACE]:    player.shoot()
        #have each enemy move closer down
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)
            
            if random.randrange(0,3*fps) == 1:
                enemy.shoot()

            if collide(enemy,player):   
                player.health -= 10
                enemies.remove(enemy)
            
            #if an enemy made it to past the bottom of the screen
            elif enemy.y + enemy.get_height() > HEIGHT:   
                lives -= 1
                enemies.remove(enemy)
            
        if player.move_lasers(-laser_vel,enemies):  score += 10

def main_menu():
    title_font = pg.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin.", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                main()
    pg.quit()  

if __name__ == "__main__":  main_menu()