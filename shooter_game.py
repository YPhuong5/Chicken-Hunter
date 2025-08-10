#Create your own shooter

from pygame import *
from random import randint

#Ehe
#Font setting:
font.init()
font1 = font.Font(None, 80)
win = font1.render('You Win!', True, (255, 254, 252))
lose = font1.render('You Lose!', True, (255, 254, 252))

font2 = font.Font(None, 20)

win_width = 800
win_height = 600
game = True
clock = time.Clock()
FPS = 60
background = transform.scale(image.load('backgroud2.jpg'), (win_width, win_height))

window = display.set_mode((win_width, win_height))
goal = 100
score = 0
missed = 0
max_lost = 10
display.set_caption("Shooter")

img_heal = transform.scale(image.load('Heart.jpg'), (40, 40))
img_speed = transform.scale(image.load('booster.png'), (40, 40))
img_boss = transform.scale(image.load('boss.png'), (80, 50))
img_enemy = transform.scale(image.load('chicken.png'), (80, 50))
img_enemy2 = transform.scale(image.load('chickenlv2.png'), (80, 50))
img_player = transform.scale(image.load('hunter.png'), (100, 100))
img_bullet = transform.scale(image.load('bullet.png'), (15, 25))
#Sound setting:
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

shooting_sound = mixer.Sound('fire.ogg')

#ENEMY SPAWN SETTING:
spawn_counter = 0
spawn_delay = randint(30,60)
MAX_ENEMIES = 6

#Chicken progression system:
chicken_level = 1
chicken_killed = 0
CHICKEN_PER_LEVEL = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
 
        self.image = player_image
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.health = 100
        self.max_health = 100
        self.base_speed = player_speed
        self.speed_boost_timer = 0
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 25, 10) 
        bullets.add(bullet)
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0 
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, chicken_type = 1):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.chicken_type = chicken_type
        self.health = chicken_type
    
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            missed += 1
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            
            
    def take_damage(self):
        self.health -= 1
        return self.health <= 0
            
class Item(GameSprite):
    def __init__(self, item_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_type = item_type
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()
                        


enemies = sprite.Group()

items = sprite.Group()
'''for i in range(1,6):
    enemy = Enemy(img_enemy , randint(80, win_width - 80), -40, 80, 50, randint(1,4))
    enemies.add(enemy)'''
    
    
    
            
bullets = sprite.Group()
            
player = Player(img_player, 370, 500, 100, 100, 15)

def draw_health_bar():
    bar_width = 20
    bar_height = 200
    bar_x = win_width - 40
    bar_y = 50
    
    draw.rect(window,(100,100,100), (bar_x, bar_y, bar_width, bar_height))
    
    health_ratio = player.health / player.max_health
    current_height = int(bar_height * health_ratio)

    #Draw health bar
    if health_ratio > 0.5:
        color = (50, 247, 47) #green
    elif health_ratio > 0.25:
        color = (255, 231, 74) #yellow
    else:
        color = (191, 17, 17) #red
        
    draw.rect(window, color, (bar_x, bar_y + bar_height - current_height, bar_width, current_height))
    
    draw.rect(window,(255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
    
    health_text = font2.render(f"{player.health}/{player.max_health}", True, (255, 255, 255))
    window.blit(health_text, (bar_x - 10, bar_y + bar_height + 10 ))

finish = False
run = True

boss_appear = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                shooting_sound.play()
                
            
    if not finish:
        
        window.blit(background,(0, 0))
            
        player.reset()
        player.update()
        
        bullets.draw(window)
        bullets.update()
        print(chicken_level, chicken_killed)
        
        items.draw(window)
        items.update()
        
        spawn_counter += 1
        if spawn_counter >= spawn_delay and len(enemies) < MAX_ENEMIES:
            if chicken_killed >= CHICKEN_PER_LEVEL and chicken_level < 4:
                chicken_level += 1
                chicken_killed = 0
                print(chicken_level)
                
            if chicken_level == 1:
                chicken_type = 1
                chicken_img = img_enemy
                chicken_speed = randint(1,3)
            elif chicken_level == 2:
                chicken_type = 2
                chicken_img = img_enemy2
                chicken_speed = randint(2,5)
            elif chicken_level == 3:
                chicken_boss = Enemy(img_boss, 300, -50, 80, 50, 5, 50)
                chicken_boss.health = 100
                boss_appear = True
                
                
                
        
            enemy = Enemy(chicken_img, randint(40, win_width - 50), -30, 80, 50, chicken_speed, chicken_type)
            enemies.add(enemy)
            spawn_counter = 0
            spawn_delay = randint(30,60)
        
        enemies.draw(window)
        enemies.update()
        
        for enemy in enemies:
            if enemy.rect.bottom >= win_height - 40:
                enemies.remove(enemy)
        
        if randint(1, 50) == 1:
            item_type = randint(1,2)
            if item_type == 1:
                item = Item('heal', img_heal, randint(80, win_width - 80), -40, 40, 40, 3)
            elif item_type == 2:
                item = Item('speed', img_speed, randint(80, win_width - 80), -40, 40, 40, 3)
            items.add(item)
        
        text = font2.render('Score: ' + str(score), 1, (95, 209, 69))
        window.blit(text, (10,20))
        
        text_lose = font2.render('Missed: '+ str(missed), 1, (95, 209, 69))
        window.blit(text_lose, (10,50))
        
        draw_health_bar()
        
        for bullet in bullets:
            for enemy in enemies:
                if sprite.collide_rect(bullet, enemy):
                    bullets.remove(bullet)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        score += enemy.chicken_type
                        chicken_killed += 1
                    break
                    
        for item in sprite.spritecollide(player,items, True):
            if item.item_type == 'heal':
                player.health += 10
                if player.health > player.max_health:
                    player.health = player.max_health
            elif item.item_type == 'speed':
                player.speed = player.base_speed *2
                player.speed_boost_timer = 200
                
        for enemy in sprite.spritecollide(player,enemies, True):
            player.take_damage(enemy.chicken_type *5)
            enemy = Enemy(img_enemy , randint(80, win_width - 80), -40, 80, 50, randint(1,6))
            enemies.add(enemy)
        
        if boss_appear == False:
            if player.health <= 0:
                finish = True
                window.blit(lose, (300,250))
        else:
            chicken_boss.update()
            if sprite.collide_rect(player, chicken_boss):
                finish = True
                window.blit(lose, (300, 250))
            if chicken_boss.health == 0:
                finish = True
                window.blit(win, (300, 250))   
            if sprite.collide_rect(bullet, chicken_boss):
                    bullets.remove(bullet)
                    chicken_boss.health -= 1
                    print(chicken_boss.health)
                    
        if player.speed_boost_timer > 0: 
            player.speed_boost_timer -= 1
            if player.speed_boost_timer == 0:
                player.speed = player.base_speed
                
            
            
    display.update()
    time.delay(50)
