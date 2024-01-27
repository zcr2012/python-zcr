from sys import exit
import pygame
from random import randrange,choice
from os import  path

def main():
    player_lives = 3
    player_health = 100
    run = True
    pygame.init()
    pygame.mixer.init()
    score = 0
    RED = (255,0,0)
    WHITE = (255,255,255)
    player_img = pygame.image.load(path.join('image','飞机.png'))
    beijing_img0 = pygame.image.load(path.join('image', '背景.PNG'))
    beijing_img = pygame.transform.scale(beijing_img0,(500,600))
    rock_img = pygame.image.load(path.join('image','陨石.PNG'))
    bullet_img = pygame.image.load(path.join('image','子弹.PNG'))
    bullet_img = pygame.image.load(path.join('image','子弹.PNG'))
    player_mini_img = pygame.transform.scale(player_img,(25,9))
    love_img = pygame.image.load(path.join('image','爱心.PNG'))


    expl_anim = {}
    expl_anim['lg'] = []
    expl_anim['sm'] = []
    for i in range(1,4):
        expl_img = pygame.image.load(path.join('image',f'爆炸{i}.PNG'))
        expl_img.set_colorkey((0,0,0))
        expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75)))
        expl_anim['sm'].append(pygame.transform.scale(expl_img, (50, 50)))
    FPS = 60

    WIDTH = 500
    HEIGHT = 600
    shoot_sound = pygame.mixer.Sound(path.join('sound', '射击.mp3 '))
    expl_sound = [
        pygame.mixer.Sound(path.join('sound', '爆炸1.mp3 ')),
        pygame.mixer.Sound(path.join('sound', '爆炸2.mp3 '))
    ]
    pygame.mixer.music.load(path.join('sound', 'main.mp3 '))
    pygame.mixer.music.set_volume(0.7)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('飞机大战')
    pygame.display.set_icon(player_mini_img)
    clock = pygame.time.Clock()





    font_name = path.join('FZDengXHJW-R.TTF')
    def draw_text(surf,text,size,x,y):
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(text,True,(255,255,255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface,text_rect)




    def new_rock():
        rock = Rock()
        all_sprite.add(rock)
        rocks.add(rock)

    def draw_health(surf,hp,x,y):
        if hp<0:
            hp = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (hp/100)*BAR_LENGTH
        outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
        fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
        pygame.draw.rect(surf,RED,fill_rect)
        pygame.draw.rect(surf,WHITE,outline_rect,2)


    def draw_live(surf,lives,img,x,y):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x+30*i
            img_rect.y = y
            surf.blit(img,img_rect)

    def draw_init():
        screen.blit(beijing_img, (0, 0))
        draw_text(screen,'太空生存战',64,WIDTH/2,HEIGHT/4)
        draw_text(screen, '← →移动飞船，空格键发射子弹', 22, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, '任意键开始游戏', 18 ,WIDTH /2, HEIGHT *3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    exit()
                elif event.type == pygame.KEYUP :
                    if event.key != pygame.K_c:
                        waiting = False



    def come_back():
        screen.blit(beijing_img, (0, 0))
        draw_text(screen, '太空生存战', 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, '暂停中，任意键继续游戏', 22, WIDTH / 2, HEIGHT / 2)
        pygame.display.update()
        waiting = True
        while waiting:

            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    exit()
                elif event.type == pygame.KEYUP:
                    if event.key != pygame.K_c:
                        waiting = False

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(player_img,(50,38))

            self.rect = self.image.get_rect()
            self.radius = 25
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-10
            self.health = 100
            self.lives = 3
            self.hidden = False
            self.hide_time = 0
        def update(self):
            if self.hidden == True and pygame.time.get_ticks() - self.hide_time > 1000:
                self.hidden = False
                self.rect.centerx = WIDTH / 2
                self.rect.bottom = HEIGHT - 10
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RIGHT] == True:
                self.rect.x += 8
            elif key_pressed[pygame.K_LEFT] == True:
                self.rect.x -= 8
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        def shoot(self):
            if not (self.hidden):
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprite.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

        def hide(self):
            self.hidden = True
            self.hide_time = pygame.time.get_ticks()
            self.rect.center = (WIDTH/2,HEIGHT+500)



    class Rock(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(rock_img,(20,30))#pygame.Surface((20,30))

            self.rect = self.image.get_rect()
            self.radius = self.rect.width /2
            self.w = self.rect.width
            self.rect.x = randrange(0,WIDTH-self.w)
            self.rect.y = randrange(-100,-40)
            self.speedy = randrange(2,10)
            self.speedx = randrange(-3, 3)
            self.rect.bottom = 2
        def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right<0:
                self.image = pygame.transform.scale(rock_img,(20,30))
                self.rect = self.image.get_rect()
                self.rect.x = randrange(0, WIDTH - self.rect.width)
                self.rect.y = randrange(-100, -40)
                self.speedy = randrange(2, 10)
                self.speedx = randrange(-3, 3)
                self.rect.bottom = 2
    class Bullet(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(bullet_img, (10, 20))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y

            self.speedy = -10


        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()
    class Explosion(pygame.sprite.Sprite):
        def __init__(self,center,size):
            pygame.sprite.Sprite.__init__(self)
            self.size = size
            self.image = expl_anim[self.size][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0

            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 40

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(expl_anim[self.size]):
                    self.kill()
                else:
                    self.image = expl_anim[self.size][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center
    class Love(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(love_img, (40, 40))

            self.rect = self.image.get_rect()

            self.w = self.rect.width
            self.rect.x = randrange(0, WIDTH - self.w)
            self.rect.y = randrange(-100, -40)
            self.speedy = randrange(2, 10)
            self.speedx = randrange(-3, 3)
            self.rect.bottom = 2

        def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
                self.image = pygame.transform.scale(love_img, (40, 40))

                self.rect = self.image.get_rect()
                self.radius = self.rect.width / 2
                self.w = self.rect.width
                self.rect.x = randrange(0, WIDTH - self.w)
                self.rect.y = randrange(-100, -40)
                self.speedy = randrange(2, 10)
                self.speedx = randrange(-3, 3)
                self.rect.bottom = 2




    all_sprite = pygame.sprite.Group()
    player = Player()
    all_sprite.add(player)
    rocks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    players = pygame.sprite.Group()
    loves = pygame.sprite.Group()
    players.add(player)

    def new_love():
        love = Love()
        all_sprite.add(love)
        loves.add(love)


    for i in range(8):
        new_rock()

    for i in range(4):

        new_love()

    pygame.mixer.music.play(-1)
    show_init = True
    running = True
    while running == True:
        if show_init:
            draw_init()


            show_init = False
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_c:


                    come_back()
                    all_sprite = pygame.sprite.Group()
                    player = Player()
                    all_sprite.add(player)
                    rocks = pygame.sprite.Group()
                    bullets = pygame.sprite.Group()
                    players = pygame.sprite.Group()
                    loves = pygame.sprite.Group()
                    players.add(player)
                    for i in range(9):
                        new_rock()
                        new_love()

        all_sprite.update()
        hits = pygame.sprite.groupcollide(bullets,rocks,True,True)
        for hit in hits:

            choice(expl_sound).play()
            score += 1
            exel = Explosion(hit.rect.center,'lg')
            all_sprite.add(exel)
            new_rock()
            if player_health <= 0:
                player_lives -= 1
                player_health = 100
                draw_health(screen, player_health, 5, 10)
                player.hide()
        hits = pygame.sprite.groupcollide(players, rocks, False,True,pygame.sprite.collide_circle)
        for hit in hits:
            player_health -= 5
            exel = Explosion(hit.rect.center,'sm')
            all_sprite.add(exel)
            new_rock()
            if player_lives == 0:
                score = 0
                player_lives = 3
                player_health = 100
                show_init = True
                all_sprite = pygame.sprite.Group()
                player = Player()
                all_sprite.add(player)
                rocks = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                players = pygame.sprite.Group()
                loves = pygame.sprite.Group()
                players.add(player)
                for i in range(9):
                    new_rock()
                    new_love()


        hits = pygame.sprite.groupcollide(bullets, loves, True, True,)
        if player_health >= 100:
            player_health = 100
        if hits:
            new_love()
            player_health += 5

        chits = pygame.sprite.groupcollide(players, loves, False, True)
        if chits:
            new_love()

        screen.blit(beijing_img,(0,0))
        all_sprite.draw(screen)
        draw_text(screen,'score:'+str(int(score)) ,18,WIDTH/2, 10)
        draw_health(screen,player_health,5,10)
        draw_live(screen,player_lives,player_mini_img,WIDTH-100,15)
        pygame.display.update()


    exit()
if __name__ == '__main__':
    main()
