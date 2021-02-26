import pygame, random, json

#set up stuff
pygame.init()

win = pygame.display.set_mode((1000, 600))

pygame.display.set_caption('Minecraft')

gameIcon = pygame.image.load("./assets/images/icon.png")
pygame.display.set_icon(gameIcon)

clock = pygame.time.Clock()

name = ''


global snc
snc = True
#fonts
reg = pygame.font.Font("./assets/fonts/reg/Minecraft.ttf", 50)
reg2 = pygame.font.Font("./assets/fonts/reg/Minecraft.ttf", 40)
reg3 = pygame.font.Font("./assets/fonts/reg/Minecraft.ttf", 30)
rb = random.randint(1, 4)
if rb == 3 or rb == 4 or rb == 1:
    c = (0,0,0)
else:
    c = (214,214,214)
phtext = reg.render('Pygame Edition', True, c)
stext = reg.render('Press Enter for A New Challenge', True, c)
ntext = reg.render('Press Enter To Begin', True, c)
pstext = reg.render('Paused', True, (0,0,0))
psitext = reg2.render('To Resume, Press P. To Quit, Press esc', True, (0,0,0))
ntextr = phtext.get_rect()
ntextr.center = (850 // 2, 1100 // 2)
phtextr = phtext.get_rect()
stextr = phtext.get_rect()
pstextr = pstext.get_rect()
psitextr = psitext.get_rect()
phtextr.center = (1000 // 2, 500 // 2)
stextr.center = (300, 550)
pstextr.center = (500, 100)
psitextr.center = (500, 300)

dtext = reg.render('You Died!', True, (0,0,0))
dtextr = dtext.get_rect()
dtextr.center = (500, 100)

detext = reg2.render('Press ESC to go to the main menu', True, (0,0,0))
detextr = dtext.get_rect()
detextr.center = (300, 500)

#images
daygpic = pygame.image.load("./assets/images/day.png")
blurpic = pygame.image.load("./assets/images/blur.png")
redblurpic = pygame.image.load("./assets/images/redblur.png")
greenblurpic = pygame.image.load("./assets/images/greenblur.png")
logopic = pygame.image.load("./assets/images/logo.png")

bgcounter = 1.0

global sound
menu = 1
sound = 1

#classes

#make the background
class bg():
    def __init__(self, bgimage, x, y):
        global bgp, rb
        bgp = pygame.transform.scale(pygame.image.load(bgimage), (1000, 700))
        win.blit(bgp, (x, y))
    def changepic(self, bgimage, x, y):
        global bgp, bgcounter, text, rb, reg, c
        bgcounter = 1.0
        bgp = pygame.transform.scale(pygame.image.load(bgimage), (1000, 700))
        text = pygame.image.load('./assets/images/text.png')
        win.blit(bgp, (x, y))
        win.blit(text, (50, -200))
        if rb == 3 or rb == 4 or rb == 1:
            c = (0,0,0)
        else:
            c = (214,214,214)
        phtext = reg.render('Pygame Edition', True, c)
        stext = reg.render('Press Enter for A New Challenge', True, c)
        ntext = reg.render('Press Enter To Begin', True, c)
        phtextr = phtext.get_rect()
        stextr = phtext.get_rect()
        phtextr.center = (1000 // 2, 500 // 2)
        stextr.center = (300, 550)
        win.blit(phtext, phtextr)
        win.blit(stext, stextr)

class block():
    def __init__(self, blockt, x, y):
        self.blocktype = blockt
        self.gx = x
        self.gy = y
        self.x = x*50
        self.y = y*50
    def sethealth(self):
        if self.blocktype == 1 or self.blocktype == 5:
            self.health = 60
        if self.blocktype == 11:
            self.health = 80
        if self.blocktype == 2 or self.blocktype == 3:
            self.health = 120
        if self.blocktype == 8:
            self.health = 10000
        if self.blocktype == 6 or self.blocktype == 7 or self.blocktype == 0 or self.blocktype == 17:
            self.health = -1
        if self.blocktype == 14 or self.blocktype == 12:
            self.health = 40
        if self.blocktype == 4:
            self.health = 120
        if self.blocktype == 9:
            self.health = 160
        if self.blocktype == 18:
            self.health = 200
        if self.blocktype == 10:
            self.health = 240
        if self.blocktype == 15 or self.blocktype == 16:
            self.health = 20
        if self.blocktype == 13:
            self.health = 40
    def damage(self):
        self.health -= 1
        print(f'Block Health: {self.health}')
        if self.blocktype == 8:
            if self.health == 7500:
                ach(6)
        if self.health == 0:
            if self.gy > 3:
                if self.blocktype == 1 or self.blocktype == 5 or self.blocktype == 14:
                    ach(1)
                if self.blocktype == 2 or self.blocktype == 3 or self.blocktype == 4 or self.blocktype == 13:
                    ach(2)
                if self.blocktype == 9:
                    ach(3)
                if self.blocktype == 18:
                    ach(4)
                if self.blocktype == 10:
                    ach(5)
                self.blocktype = 17
            else:
                self.blocktype = 0
            if blocklist[self.gx][self.gy-1].blocktype == 6:
                self.blocktype = 6
            if blocklist[self.gx][self.gy-1].blocktype == 7:
                self.blocktype = 7

class timer():
    def __init__(self):
        self.ts = 0
        self.sec = 0
        self.min = 0
    def run(self):
        self.ts += 1
        if self.ts == 1000:
            self.ts = 0
            self.sec += 1
        if self.sec == 60:
            self.sec = 0
            self.min += 1
    def get(self):
        if self.sec < 10:
            self.dis = f'{self.min}:0{self.sec}'
        else:
            self.dis = f'{self.min}:{self.sec}'
        return self.dis
    def display(self):
        dpstext = reg3.render(f'Time: {self.get()}', True, (0,0,0))
        dpstextr = dpstext.get_rect()
        dpstextr.center = (920,50)
        win.blit(dpstext, dpstextr)


#player
class playero():
    def __init__(self):
        global csprite
        global sfire, swater0, swater1, swater2, swater3, swater4, swater5, sfire1, sfire2, sfire3
        global drownpic, heartpic, poppic
        self.x = 10.0
        self.y = 3
        standing = pygame.image.load('./assets/sprites/sprite.png')
        csprite = standing
        self.fire = False
        self.down = False
        self.waterc = 0.0
        swater0 = pygame.image.load('./assets/sprites/water0.png')
        swater1 = pygame.image.load('./assets/sprites/water1.png')
        swater2 = pygame.image.load('./assets/sprites/water2.png')
        swater3 = pygame.image.load('./assets/sprites/water3.png')
        swater4 = pygame.image.load('./assets/sprites/water4.png')
        swater5 = pygame.image.load('./assets/sprites/water5.png')
        sfire1 = pygame.image.load(f'./assets/sprites/fire1.png')
        sfire2 = pygame.image.load(f'./assets/sprites/fire2.png')
        sfire3 = pygame.image.load(f'./assets/sprites/fire3.png')
        drownpic = pygame.image.load(f'./assets/sprites/drown.png')
        heartpic = pygame.image.load(f'./assets/sprites/heart.png')
        poppic = pygame.image.load(f'./assets/sprites/pop.png')
        self.watercount = 8.0
        self.health = 8.0
    def drawsprite(self):
        global csprite, sfire
        win.blit(csprite, (self.x*50-100, self.y*50-40))
        if player.fire == True:
            fn = random.randint(1,3)
            if fn == 1:
                sfire = sfire1
            if fn == 2:
                sfire = sfire2
            if fn == 3:
                sfire = sfire3
            win.blit(sfire, (self.x*50-100, self.y*50-40))
        if player.water == True:
            player.waterc = player.waterc + 0.01
            if int(player.waterc) == 6:
                player.waterc = 1.0
            if int(player.waterc) == 0:
                win.blit(swater0, (self.x*50-100, self.y*50-45))
            if int(player.waterc) == 1:
                win.blit(swater1, (self.x*50-100, self.y*50-45))
            if int(player.waterc) == 2:
                win.blit(swater2, (self.x*50-100, self.y*50-45))
            if int(player.waterc) == 3:
                win.blit(swater3, (self.x*50-100, self.y*50-45))
            if int(player.waterc) == 4:
                win.blit(swater4, (self.x*50-100, self.y*50-45))
            if int(player.waterc) == 5:
                win.blit(swater5, (self.x*50-100, self.y*50-45))
    def deathscreen(self, case):
        if case == 1:
            dctext = reg2.render('The Player Tried to Swim in Lava', True, (0,0,0))
        if case == 2:
            dctext = reg2.render('The Player Thought That They Were Aqua Man', True, (0,0,0))
        dctextr = dctext.get_rect()
        dctextr.center = (500, 300)
        win.blit(dctext, dctextr)
                    


#functions
def genblock(direction):
    findingstuff = True
    columns = 0
    while findingstuff: #finds how many columns there are
        try:
            a = blocklist[columns][1]
            columns += 1
        except:
            findingstuff = False
    columns -= 1 * direction

def playsound(soundb, soundid):
    global sound
    if soundb == 1:
        if soundid == 0:
            pygame.mixer.music.load('./assets/music/wethands.mp3')
            pygame.mixer.music.play(-1)
        if soundid == 1:
            pygame.mixer.music.load('./assets/music/cow.mp3')
            pygame.mixer.music.play(-1)
        if soundid == 2:
            pygame.mixer.music.load('./assets/music/sad.mp3')
            pygame.mixer.music.play(-1)
        if soundid == 3:
            pygame.mixer.music.load('./assets/music/victory.mp3')
            pygame.mixer.music.play(0)
    if sound == 0:
        mutesound()

def mutesound():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()

def ach(id):
    global xp
    if id == 1:
        xp += 1
    if id == 2:
        xp += 5
    if id == 3:
        xp += 10
    if id == 4:
        xp += 15
    if id == 5:
        xp += 20
    if id == 6:
        xp += 100
    if id == 7:
        xp += 50

#make homescreen bg        
bgobj = bg('./assets/images/bg{}.jpg'.format(rb), 0, 0)
text = pygame.image.load('./assets/images/text.png')
win.blit(text, (50, -200))



win.blit(phtext, phtextr)
win.blit(stext, stextr)


#sound
soundv = int(open('./assets/settings/sound.txt', 'r').read())
try:
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
except:
    open('./assets/settings/sound.txt', 'w').write('0')
    soundv = 0
playsound(soundv, 0)

run = True

while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if sound == 1:
                        mutesound()
                        sound = 0
                    elif sound == 0:
                        sound = 1
                        unpause()
                if menu == 2:
                    if name == '' or name.replace(' ', '') == '':
                        namef = 0
                    else:
                        namef = 1
                    if event.key == pygame.K_RETURN:
                        if namef == 1:
                            menu = 6
                        else:
                            nf = reg2.render("You can't have an empty name!", True, c)
                            nfr = nf.get_rect()
                            nfr.center = (500, 300)
                            win.blit(nf, nfr)
                            name = ''
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                        win.blit(bgp, (0, 0))
                        nntext = reg.render('Type in your name:', True, c)
                        nntextr = nntext.get_rect()
                        nntextr.center = (500, 100)
                        nametext = reg2.render(name, True, c)
                        nametextr = nametext.get_rect()
                        nametextr.center = (500, 200)
                        win.blit(nntext, nntextr)
                        win.blit(nametext, nametextr)
                        win.blit(ntext, ntextr)
                    else:
                        if len(name) < 11:
                            name += event.unicode
                            win.blit(bgp, (0, 0))
                            nntext = reg.render('Type in your name:', True, c)
                            nntextr = nntext.get_rect()
                            nntextr.center = (500, 100)
                            nametext = reg2.render(name, True, c)
                            nametextr = nametext.get_rect()
                            nametextr.center = (500, 200)
                            win.blit(nntext, nntextr)
                            win.blit(nametext, nametextr)
                            win.blit(ntext, ntextr)
                if menu == 1:
                    if event.key == pygame.K_RETURN:
                        win.blit(bgp, (0, 0))
                        nntext = reg.render('Type in your name:', True, c)
                        nntextr = nntext.get_rect()
                        nntextr.center = (500, 100)
                        win.blit(nntext, nntextr)
                        win.blit(ntext, ntextr)
                        menu = 2
                if event.key == pygame.K_p:
                    if menu == 3 or menu == 4:
                        if menu != 4:
                            win.blit(blurpic, (0,0))
                            win.blit(pstext, pstextr)
                            win.blit(psitext, psitextr)
                            win.blit(logopic, (200,500))
                            menu = 4
                        else:
                            menu = 3
                if event.key == pygame.K_ESCAPE:
                    if menu == 4 or menu == 5:
                        bgobj = bg('./assets/images/bg{}.jpg'.format(rb), 0, 0)
                        text = pygame.image.load('./assets/images/text.png')
                        win.blit(text, (50, -200))
                        win.blit(phtext, phtextr)
                        win.blit(stext, stextr)
                        name = ''
                        playsound(soundv, 0)
                        xp = 0
                        menu = 1

    if menu == 1:
        bgcounter+=1
            
        if bgcounter == 300:
            rb = random.randint(1,4)
            bgobj.changepic('./assets/images/bg{}.jpg'.format(rb), 0, 0)
    if menu == 2:
        pass
            
        
    if menu == 6:
            win.blit(daygpic, (0,0))
            menu = 3
            playsound(soundv, 1)
            #make the default chunk

            flowcount = 0
            lblockid = 1
            jumping = False
            jumpcount = 1.0
            xp = 0
            
            #make the array for the blocks
            global blocklist
            blocklist = [[0 for _ in range(13)] for _ in range(21)]

            for num in range(21):
                for num2 in range(13):
                    blockidn = f'b{lblockid}'
                    blockidn = block(0, num, num2)
                    blocklist[num][num2] = blockidn
                    lblockid += 1

            #make the general stuff
            for num in range(0, 21):
                blocklist[num][12].blocktype = 8
                for num2 in range(4, 12):
                    sn = random.randint(1,2)
                    if sn == 1:
                        blocklist[num][num2].blocktype = 1
                    if sn == 2:
                        blocklist[num][num2].blocktype = 5

            for num in range(0, 21):
                for num2 in range(7, 12):
                    sn = random.randint(1,8)
                    if sn == 1 or sn == 3 or sn == 4 or sn == 7:
                        blocklist[num][num2].blocktype = 2
                    if sn == 2 or sn == 5 or sn == 6:
                        blocklist[num][num2].blocktype = 3
                    if sn == 8:
                        blocklist[num][num2].blocktype = 4
                for num2 in range(9, 12):
                    sn = random.randint(1,16)
                    if sn == 16:
                        blocklist[num][num2].blocktype = 9
                for num2 in range(8, 12):
                    sn = random.randint(1,24)
                    if sn == 24:
                        blocklist[num][num2].blocktype = 18
                for num2 in range(10, 12):
                    sn = random.randint(1,28)
                    if sn == 28:
                        blocklist[num][num2].blocktype = 10
            for num in range(0, 21):
                sn = random.randint(1,4)
                if sn == 1:
                    blocklist[num][7].blocktype = 5
                if sn == 2:
                    blocklist[num][7].blocktype = 1


            #chunk geogrphic features

            ocean = random.randint(1,16)
            
            if ocean != 2:
                fr = random.randint(1, 4)
                if fr == 2:
                    #generate a lake
                    depth = random.randint(1, 2)
                    x = random.randint(1, 15)
                    width = random.randint(1, 5)
                    for num in range(width):
                        blocklist[x+num][4].blocktype = 6
                        for dnum in range(depth):
                            blocklist[x+num][dnum+4].blocktype = 6
                fr = random.randint(1, 10)
                if fr == 8:
                    #make a lava lake
                    depth = random.randint(1, 2)
                    x = random.randint(1, 15)
                    width = random.randint(1, 5)
                    for num in range(width):
                        if blocklist[x+num][4].blocktype == 6:
                            blocklist[x+num][4].blocktype = 2
                        else:
                            blocklist[x+num][4].blocktype = 7
                        for dnum in range(depth):
                            if blocklist[x+num][4+dnum].blocktype == 6:
                                blocklist[x+num][4+dnum].blocktype = 2
                            if blocklist[x+num][4+dnum].blocktype == 2:
                                blocklist[x+num][4+dnum].blocktype = 2
                            else:
                                blocklist[x+num][4+dnum].blocktype = 7
                fr = random.randint(1, 2)
                if fr == 2:
                    #generate lava underground
                    width = random.randint(1, 3)
                    depth = random.randint(1, 2)
                    x = random.randint(1, 17)
                    y = random.randint(9, 10)
                    for num in range(width):
                        blocklist[x+num][y].blocktype = 7
                        for dnum in range(depth):
                            blocklist[x+num][y+dnum].blocktype = 7

                fr = random.randint(1, 3)
                if fr == 3:
                    #generate a tree
                    barkheight = random.randint(1,2)
                    barkly = 3
                    barkx = random.randint(1, 9)
                    leafh = 2
                    leafw = 3
                    for num in range(barkheight):
                        blocklist[barkx][barkly-num].blocktype = 11
                    for num in range(leafh):
                        blockidn = f'b{lblockid}'
                        blockidn = block(12, barkx, barkly-barkheight-num)
                        blocklist[barkx][barkly-barkheight-num] = blockidn
                        lblockid += 1
                    for num in range(1, 4):
                        if num == 1:
                            blocklist[barkx-1][barkly-barkheight].blocktype = 12
                        if num == 3:
                            blocklist[barkx+1][barkly-barkheight].blocktype = 12
                fr = random.randint(1,2)
                if fr == 2:
                    #generate a hill
                    hx = random.randint(1, 10)
                    width = random.randint(1, 10)
                    depth = random.randint(1,2)
                    for num in range(width):
                        blocklist[hx+num][3].blocktype = 1
                    if depth == 2:
                        for num in range(hx+1, width-random.randint(1,2)):
                            blocklist[num][2].blocktype = 1
                fr = random.randint(1,4)
                if fr == 4:
                    #generate a cave
                    y = random.randint(8, 9)
                    x = random.randint(0, 3)
                    length = random.randint(10,17)
                    depth = random.randint(1,3)
                    rychange = random.randint(0,2)
                    surface = random.choice([True, False])
                    print(length)
                    print(x)
                    for num in range(x,length):
                        for num2 in range(y, y+depth):
                            try:
                                blocklist[num][num2].blocktype = 17
                            except:
                                print(num)
                                print(num2)
                    if surface == True:
                        lr = random.randint(0,1)
                        if lr == 0:
                            num3 = x+1
                        if lr == 1:
                            num3 = x+length-2
                        for num in range(4, y):
                            for num2 in range(num3-2, num3):
                                blocklist[num2][num].blocktype = 17
                for num in range(0, 21):
                    blocklist[num][11].blocktype = 8
                            
                            
                        
                        
            else:
                #ocean
                for num in range(0,21):
                    for num2 in range(4, 12):
                        blocklist[num][num2].blocktype = 6
                        if num == 0:
                            blocklist[num][num2].blocktype = 14
                        if num == 20:
                            blocklist[num][num2].blocktype = 14
                    fr = random.randint(1,2)
                    if fr == 1:
                        blocklist[num][11].blocktype = 14
                    if fr == 2:
                        blocklist[num][11].blocktype = 13  
                    fr = random.randint(1, 3)
                    if fr == 3:
                        fr = random.randint(1,3)
                        blocklist[num][10].blocktype = 14
                        if fr == 3:
                            if num != 0 and num != 20:
                                blocklist[num][9].blocktype = random.choice([15,16])
                    if fr == 1:
                        if num != 0 and num != 20:
                            blocklist[num][10].blocktype = random.choice([15,16])
                for num in range(0, 21):
                    blocklist[num][12].blocktype = 8
            for num in range(21):
                for num2 in range(13):
                    blocklist[num][num2].sethealth()
                    
            
            
            #sprite stuff
            player = playero()
                    
            #load blocks
            dirt = pygame.image.load('./assets/blocks/dirt.png')
            dirt2 = pygame.image.load('./assets/blocks/dirt2.png')
            grass = pygame.image.load('./assets/blocks/grass.png')
            stone = pygame.image.load('./assets/blocks/stone.png')
            stone2 = pygame.image.load('./assets/blocks/stone2.png')
            coal = pygame.image.load('./assets/blocks/coal.png')
            iron = pygame.image.load('./assets/blocks/iron.png')
            sand = pygame.image.load('./assets/blocks/sand.png')
            water = pygame.image.load('./assets/blocks/water.png')
            waterfill = pygame.image.load('./assets/blocks/waterfill.png')
            lava = pygame.image.load('./assets/blocks/lava.png')
            clava = pygame.image.load('./assets/blocks/clava.png')
            lavafill = pygame.image.load('./assets/blocks/lavafill.png')
            bedrock = pygame.image.load('./assets/blocks/bedrock.png')
            diamond = pygame.image.load('./assets/blocks/diamond.png')
            bark = pygame.image.load('./assets/blocks/bark.png')
            leaf = pygame.image.load('./assets/blocks/leaves.png')
            gravel = pygame.image.load('./assets/blocks/gravel.png')
            reef = pygame.image.load('./assets/blocks/reef.png')
            reef2 = pygame.image.load('./assets/blocks/reef2.png')
            stonebg = pygame.image.load('./assets/blocks/stonebg.png')
            gold = pygame.image.load('./assets/blocks/gold.png')
            blockout = pygame.image.load('./assets/blocks/whiteout.png')
            blockhold = pygame.image.load('./assets/blocks/blockhold.png')


            #solid blocks
            solidblocks = [1,2,3,4,5,8,9,10,11,12,13,14, 18]
            wb = [15,16,6]
            ab = [0,17]
            lb = [7]

            #camera offset
            global offset
            offset = 0.0

            #timer
            gtimer = timer()
    if menu == 3:
        #do stuff with keys here
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.blocked = False
            if player.x+0.80:
                offsets = 0.0
                while offsets < offset:
                    offsets = offsets + 50.0
                if offsets > offset:
                    offsets = offsets - 50
                offseta = offset - offsets
                xoffset = int(offset/50)-2
                player.blockx = int(player.x + xoffset + (offseta/50))
                player.blockxr = int(player.x + xoffset + 0.96 + (offseta/50))
                if blocklist[int(player.blockxr+0.4)][int(player.y-.98)].blocktype in solidblocks:
                    player.blocked = True
                if blocklist[int(player.blockxr+0.4)][int(player.y)].blocktype in solidblocks:
                    player.blocked = True
                if blocklist[int(player.blockxr+0.4)][int(player.y+.98)].blocktype in solidblocks:
                    player.blocked = True
            if player.blocked == False:
                if player.x > 16.0:
                    offset = offset+2.5
                else:
                    player.x += .15
                #check if a new section is needed to be generated
                if int(columns-1)*50.0-offset < 1000: #checks if the column with the highest x is still on the screen
                    blocklist.extend([0 for _ in range(12)] for _ in range(20)) #generate more blocks if its not
                    for num in range(columns, columns+20):
                        for num2 in range(12):
                            blockidn = f'b{lblockid}'
                            blockidn = block(0, num, num2)
                            blocklist[num][num2] = blockidn
                            lblockid += 1
                        for num2 in range(4, 12):
                            sn = random.randint(1,2)
                            if sn == 1:
                                blocklist[num][num2].blocktype = 1
                            if sn == 2:
                                blocklist[num][num2].blocktype = 5
                        for num2 in range(7, 12):
                            sn = random.randint(1,8)
                            if sn == 1 or sn == 3 or sn == 4 or sn == 7:
                                blocklist[num][num2].blocktype = 2
                            if sn == 2 or sn == 5 or sn == 6:
                                blocklist[num][num2].blocktype = 3
                            if sn == 8:
                                blocklist[num][num2].blocktype = 4
                        for num2 in range(8, 12):
                            sn = random.randint(1,16)
                            if sn == 16:
                                blocklist[num][num2].blocktype = 9
                        for num2 in range(9, 12):
                            sn = random.randint(1,24)
                            if sn == 24:
                                blocklist[num][num2].blocktype = 18
                        for num2 in range(10, 12):
                            sn = random.randint(1,28)
                            if sn == 28:
                                blocklist[num][num2].blocktype = 10
                    for num in range(columns, columns+20):
                        sn = random.randint(1,4)
                        if sn == 1:
                            blocklist[num][7].blocktype = 5
                        if sn == 2:
                            blocklist[num][7].blocktype = 1


                    #geogrphic features
                    fr = random.randint(1, 4)
                    if fr == 2:
                        #generate a lake
                        depth = random.randint(1, 2)
                        x = random.randint(1, 15)
                        width = random.randint(1, 5)
                        for num in range(width):
                            blocklist[columns+x+num][4].blocktype = 6
                            for dnum in range(depth):
                                blocklist[columns+x+num][4+dnum].blocktype = 6
                    fr = random.randint(1, 10)
                    if fr == 8:
                        #make a lava lake
                        depth = random.randint(1, 2)
                        x = random.randint(1, 15)
                        width = random.randint(1, 5)
                        for num in range(width):
                            if blocklist[columns+x+num][4].blocktype == 6:
                                blocklist[columns+x+num][4].blocktype = 2 
                            else:
                                blocklist[columns+x+num][4].blocktype = 7
                            for dnum in range(depth):
                                if blocklist[columns+x+num][4+dnum].blocktype == 6:
                                    blocklist[columns+x+num][4+dnum].blocktype = 2
                                if blocklist[columns+x+num][4+dnum].blocktype == 2:
                                    blocklist[columns+x+num][4+dnum].blocktype = 2
                                else:
                                    blocklist[columns+x+num][4+dnum].blocktype = 7
                    fr = random.randint(1, 2)
                    if fr == 2:
                        #generate lava underground
                        width = random.randint(1, 3)
                        depth = random.randint(1, 2)
                        x = random.randint(1, 17)
                        y = random.randint(9, 10)
                        for num in range(width):
                            blocklist[columns+x+num][y].blocktype = 7
                            for dnum in range(depth):
                                blocklist[columns+x+num][y+dnum].blocktype = 7
                    fr = random.randint(1,2)
                    if fr == 2:
                        #generate a hill
                        hx = random.randint(1, 10)
                        width = random.randint(1, 10)
                        depth = random.randint(1,2)
                        for wnum in range(width):
                            blocklist[columns+hx+wnum][3].blocktype = 1
                        if depth == 2:
                            xrem = random.randint(0,1)
                            oxrem = random.randint(0,2)
                            for wnum in range(hx+xrem, width-oxrem):
                                blocklist[columns+wnum][2].blocktype = 1
                    for num in range(columns, columns+20):
                        blocklist[num][11].blocktype = 8
                    for num in range(columns, columns+20):
                        for num2 in range(12):
                            blocklist[num][num2].sethealth()
                    fr = random.randint(1,4)
                    if fr == 4:
                        #generate a cave
                        y = random.randint(8, 9)
                        x = random.randint(0, 3)
                        length = random.randint(10,17)
                        depth = random.randint(1,3)
                        rychange = random.randint(0,2)
                        surface = True#random.choice([True, False])
                        print(length)
                        print(x)
                        for num in range(x+columns,length+columns+x):
                            for num2 in range(y, y+depth):
                                try:
                                    blocklist[num][num2].blocktype = 17
                                except Exception as e:
                                    print(e)
                        if surface == True:
                            lr = random.randint(0,1)
                            if lr == 0:
                                num3 = x+1+columns
                            if lr == 1:
                                num3 = x+length+columns-2
                            for num in range(4, y):
                                for num2 in range(num3-2, num3):
                                    blocklist[num2][num].blocktype = 17
                    for num in range(columns, columns+20):
                        blocklist[num][11].blocktype = 8
                    
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.blocked = False
            offsets = 0.0
            while offsets < offset:
                offsets = offsets + 50.0
            if offsets > offset:
                offsets = offsets - 50
            offseta = offset - offsets
            xoffset = int(offset/50)-2
            player.blockx = int(player.x + xoffset + (offseta/50)-0.2)
            if blocklist[int(player.blockx+0.4)][int(player.y-.98)].blocktype in solidblocks:
                player.blocked = True
            if blocklist[int(player.blockx+0.4)][int(player.y)].blocktype in solidblocks:
                player.blocked = True
            if blocklist[int(player.blockx+0.4)][int(player.y+.98)].blocktype in solidblocks:
                player.blocked = True
            if player.blocked == False:
                if player.x < 7.0:
                    if int(offset) == 0:
                        if not int(player.x) == 1:
                            player.x -= .15
                    else:
                        offset = offset-2.5
                else:
                    player.x -= .15

        #see if player is on top of lava
        offsets = 0.0
        while offsets < offset:
            offsets = offsets + 50.0
        if offsets > offset:
            offsets = offsets - 50
        offseta = offset - offsets
        xoffset = int(offset/50)-2
        player.blockx = int(player.x + xoffset + (offseta/50))
        player.blockxr = int(player.x + xoffset + 0.80 + (offseta/50))
        player.fire = False
        if blocklist[player.blockx][int(player.y+1)].blocktype == 7 and blocklist[player.blockxr][int(player.y+1)].blocktype == 7:
            player.fire = True
            player.y += 0.01
            player.y = round(player.y * 100) / 100
        #see if player is in lava
        if blocklist[player.blockx][int(player.y)].blocktype == 7 and blocklist[player.blockxr][int(player.y)].blocktype == 7:
            player.fire = True
            
        player.water = False
        if blocklist[player.blockx][int(player.y+1)].blocktype in wb and blocklist[player.blockxr][int(player.y+1)].blocktype in wb:
            player.water = True
            player.y += 0.01
            player.y = round(player.y * 100) / 100
        #see if player is in water
        if blocklist[player.blockx][int(player.y)].blocktype in wb and blocklist[player.blockxr][int(player.y)].blocktype in wb:
            player.water = True

        #space bar
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if player.fire == True or player.water == True:
                if blocklist[int(player.blockx)][int(player.y+.9)].blocktype == 7 and not blocklist[int(player.blockx)][int(player.y-.9)].blocktype in solidblocks and not blocklist[int(player.blockxr)][int(player.y-.9)].blocktype in solidblocks:
                    player.y = player.y - 0.1
                    player.y = round(player.y * 10) / 10
                if blocklist[int(player.blockx)][int(player.y+.9)].blocktype in wb and not blocklist[int(player.blockx)][int(player.y-.9)].blocktype in solidblocks and not blocklist[int(player.blockxr)][int(player.y-.9)].blocktype in solidblocks:
                    player.y = player.y - 0.1
                    player.y = round(player.y * 10) / 10
            else:
                if jumping == False:
                    if not blocklist[int(player.blockx)][int(player.y+1.08)].blocktype in ab or not blocklist[int(player.blockxr)][int(player.y+1.08)].blocktype in ab:
                        if not blocklist[int(player.blockx)][int(player.y+1.08)].blocktype == 6 or not blocklist[int(player.blockxr)][int(player.y+1.08)].blocktype == 6:
                            if not blocklist[int(player.blockx)][int(player.y+1.08)].blocktype == 7 or not blocklist[int(player.blockxr)][int(player.y+1.08)].blocktype == 7:
                                jumping = True
        #jumping
        if jumping == True:
            if jumpcount > 0.0 and player.down == False:
                if not blocklist[int(player.blockx)][int(player.y-1.0001)].blocktype in solidblocks and not blocklist[int(player.blockxr)][int(player.y-1.0001)].blocktype in solidblocks:
                    jumpcount -= 0.2
                    player.y -= 0.2
                    player.y = round(player.y * 10) / 10
                else:
                    player.down = True
            else:
                if not blocklist[int(player.blockx)][int(player.y+1.2)].blocktype in solidblocks and not blocklist[int(player.blockxr)][int(player.y+1.2)].blocktype in solidblocks:
                    player.down = True
                    jumpcount += 0.2
                    player.y += 0.2
                    player.y = round(player.y * 10) / 10
                else:
                    jumpcount = 1.0
            if jumpcount == 1.0:
                jumping = False
                player.down = False

        #set the y offset

                
        offsets = 0.0
        while offsets < offset:
            offsets = offsets + 50.0
        if offsets > offset:
            offsets = offsets - 50
        offseta = offset - offsets
        xoffset = int(offset/50)-2
        player.blockx = int(player.x + xoffset + (offseta/50))
        player.blockxr = int(player.x + xoffset + 0.80 + (offseta/50))
        if jumping == False:
            if blocklist[int(player.blockx)][int(player.y+1.08)].blocktype in ab and blocklist[int(player.blockxr)][int(player.y+1.08)].blocktype in ab:
                player.y += 0.1
                player.y = round(player.y * 10) / 10

        offsets = 0.0
        while offsets < offset:
            offsets = offsets + 50.0
        if offsets > offset:
            offsets = offsets - 50
        offseta = offset - offsets
        xoffset = int(offset/50)-2
        player.blockx = int(player.x + xoffset + (offseta/50))
        player.blockxr = int(player.x + xoffset + 0.96 + (offseta/50))
        
        #breaking blocks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            mouseb =(int(mouse[0]/50 + xoffset + offseta/50)+1, int(mouse[1]/50))
            if mouseb[0]+1 >= player.blockx-5 and mouseb[0]+1 <= player.blockx+5:
                if mouseb[1] >= int(player.y)-5 and mouseb[1] <= int(player.y)+5:
                    blocklist[mouseb[0]+1][mouseb[1]].damage()

                
        #draw screen
        win.blit(daygpic, (0,0))
        columns = len(blocklist)
        if xoffset > 0.0:
            xoffsetsr = xoffset+3
        else:
            xoffsetsr = xoffset+2
    
        for num3 in range(int(int(xoffsetsr-1)), int(xoffsetsr)+21):
                try:
                    for num4 in range(12):
                        if blocklist[num3][num4].blocktype == 1:
                            win.blit(dirt, (num3*50-offset, num4*50))
                            if blocklist[num3][num4-1].blocktype == 0:
                                win.blit(grass, (num3*50-offset, num4*50))
                            if blocklist[num3][num4-1].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                            if blocklist[num3-1][num4].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = 14
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3+1][num4].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = 14
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3-1][num4-1].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = 14
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3+1][num4-1].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = 14
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3][num4-1].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3-1][num4].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3+1][num4].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3-1][num4-1].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3+1][num4-1].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                        if blocklist[num3][num4].blocktype == 2:
                            win.blit(stone, (num3*50-offset, num4*50))
                        if blocklist[num3][num4].blocktype == 3:
                            win.blit(stone2, (num3*50-offset, num4*50))
                        if blocklist[num3][num4].blocktype == 4:
                            win.blit(coal, (num3*50-offset, num4*50))
                        if blocklist[num3][num4].blocktype == 5:
                            win.blit(dirt2, (num3*50-offset, num4*50))
                            if blocklist[num3][num4-1].blocktype == 0:
                                win.blit(grass, (num3*50-offset, num4*50))
                            if blocklist[num3][num4-1].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                            if blocklist[num3-1][num4].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                            if blocklist[num3+1][num4].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                            if blocklist[num3-1][num4-1].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                            if blocklist[num3+1][num4-1].blocktype == 6:
                                win.blit(sand, (num3*50-offset, num4*50))
                            if blocklist[num3][num4-1].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3-1][num4].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3+1][num4].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3-1][num4-1].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                            if blocklist[num3+1][num4-1].blocktype == 7:
                                win.blit(stone, (num3*50-offset, num4*50))
                                blocklist[num3][num4].blocktype = random.randint(2,3)
                                blocklist[num3][num4].sethealth()
                        if blocklist[num3][num4].blocktype == 6:
                            if blocklist[num3][num4-1].blocktype == 0:
                                if blocklist[num3][num4+1].blocktype in ab:
                                    win.blit(water, (num3*50-offset, (num4+1)*50))
                                else:
                                    win.blit(water, (num3*50-offset, num4*50))
                            else:
                                win.blit(waterfill, (num3*50-offset, num4*50))
                        if blocklist[num3][num4].blocktype == 7:
                            lavad = False
                            if blocklist[num3][num4-1].blocktype == 6:
                                pygame.draw.rect(win, (178,190,181), (num3*50-offset, num4-1*50, 50, 50))
                                pygame.draw.rect(win, (178,190,181), (num3*50-offset, num4-1*50, 50, 50))
                                blocklist[num31][num4-1].blocktype = 2
                                blocklist[num3][num4].blocktype = 2
                                lavad = True
                            if blocklist[num3-1][num4].blocktype == 6:
                                pygame.draw.rect(win, (178,190,181), (num3-1*50-offset, num4*50, 50, 50))
                                pygame.draw.rect(win, (178,190,181), (num3-1*50-offset, num4*50, 50, 50))
                                blocklist[num3-1][num4].blocktype = 2
                                blocklist[num3][num4].blocktype = 2
                                lavad = True
                            if blocklist[num3+1][num4].blocktype == 6:
                                pygame.draw.rect(win, (178,190,181), (num3+1*50-offset, num4*50, 50, 50))
                                pygame.draw.rect(win, (178,190,181), (num3+1*50-offset, num4*50, 50, 50))
                                blocklist[num3+1][num4].blocktype = 2
                                blocklist[num3][num4].blocktype = 2
                                lavad = True
                            if lavad == False:
                                if blocklist[num3][num4-1].blocktype == 0:
                                    win.blit(lava, (num3*50-offset, num4*50))
                                elif blocklist[num3][num4-1].blocktype == 17:
                                    win.blit(clava, (num3*50-offset, num4*50))
                                else:
                                    win.blit(lavafill, (num3*50-offset, num4*50))
                        if blocklist[num3][num4].blocktype == 8:
                            win.blit(bedrock, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 9:
                            win.blit(iron, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 10:
                            win.blit(diamond, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 11:
                            win.blit(bark, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 12:
                            win.blit(leaf, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 13:
                            win.blit(gravel, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 14:
                            win.blit(sand, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 15:
                            win.blit(reef, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 16:
                            win.blit(reef2, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 17:
                            win.blit(stonebg, (num3*50-offset,num4*50))
                        if blocklist[num3][num4].blocktype == 18:
                            win.blit(gold, (num3*50-offset,num4*50))
                except IndexError:
                    pass
                offsets = 0.0
                while offsets < offset:
                    offsets = offsets + 50.0
                if offsets > offset:
                    offsets = offsets - 50
                offseta = offset - offsets
                xoffset = int(offset/50)-2
                player.blockx = int(player.x + xoffset + (offseta/50))
                player.blockxr = int(player.x + xoffset + 0.96 + (offseta/50))
                mouse = pygame.mouse.get_pos()
                mouseb =(int(mouse[0]/50 + xoffset + offseta/50)+1, int(mouse[1]/50))
                if mouseb[0] <= 1:
                    mouseb = (mouseb[0]-1, mouseb[1])
        
                if mouseb[0]+1 >= player.blockx-5 and mouseb[0]+1 <= player.blockx+5:
                    if mouseb[1] >= int(player.y)-5 and mouseb[1] <= int(player.y)+5:
                        if not blocklist[mouseb[0]+1][mouseb[1]].blocktype in ab and not blocklist[mouseb[0]+1][mouseb[1]].blocktype == 6 and not blocklist[mouseb[0]+1][mouseb[1]].blocktype in lb:
                            if not event.type == pygame.MOUSEBUTTONDOWN:
                                win.blit(blockout, (((mouseb[0]+1)*50)-offset, mouseb[1]*50))
                            else:
                                win.blit(blockhold, (((mouseb[0]+1)*50)-offset, mouseb[1]*50))
                                win.blit(blockout, (((mouseb[0]+1)*50)-offset, mouseb[1]*50))
                            
                
                #sprite
                player.drawsprite()
                    #to-do:
                    #make a save hotkey
                if player.water == True:
                    for n in range(int(player.watercount)):
                        win.blit(drownpic, (n*25, 25))
                    try:
                        if player.watercount != 8.0 and int(player.watercount) != 0 and int(str(player.watercount)[:6][-4:]) > 9750:
                            win.blit(poppic, ((int(player.watercount))*25, 25))
                    except:
                        print(player.watercount)

                if player.fire == True:
                    player.health -= 0.0008 

                        
                for n in range(int(player.health)):
                        win.blit(heartpic, (n*25, 0))
                    
                        
                if blocklist[player.blockx][int(player.y)].blocktype in wb:
                    if int(player.watercount) != 0:
                        player.watercount -= 0.0002
                    else:
                        player.health -= 0.0002

                if int(player.health) == 1:
                    try:
                        if oh == 1:
                            pass
                    except:
                        ach(7)
                        oh = 1
                

                if int(player.health) == 0:
                    menu = 5
                    win.blit(redblurpic, (0,0))
                    playsound(soundv, 2)
                    win.blit(dtext, dtextr)
                    win.blit(detext, detextr)
                    if player.fire == True:
                        player.deathscreen(1)
                    if player.water == True:
                        player.deathscreen(2)

                if player.water == False and int(player.watercount) != 8:
                    player.watercount = 8
                #timer
                gtimer.run()
                gtimer.display()
                
            

    

    clock.tick(60) #60 fps
    if menu == 3:
        fpstext = reg3.render(f'FPS: {int(clock.get_fps())}', True, (0,0,0))
        fpstextr = fpstext.get_rect()
        fpstextr.center = (940,20)
        win.blit(fpstext, fpstextr)
        if random.randint(1,200) == 1:
            ach(1)
        fpstext = reg3.render(f'XP: {xp}/500', True, (0,0,0))
        fpstextr = fpstext.get_rect()
        fpstextr.center = (900,80)
        win.blit(fpstext, fpstextr)
        if xp > 499:
            win.blit(greenblurpic, (0,0))
            playsound(soundv, 3)
            menu = 8
    if menu == 8:
        vtext = reg.render(f'Victory!', True, (0,0,0))
        vtextr = vtext.get_rect()
        vtextr.center = (500, 300)
        win.blit(vtext, vtextr)
        vttext = reg2.render(f'Time: {gtimer.get()}', True, (0,0,0))
        vttextr = vttext.get_rect()
        vttextr.center = (500, 400)
        win.blit(vttext, vttextr)
        win.blit(vtext, vtextr)
        vtttext = reg2.render(f'Thanks for Playing!', True, (0,0,0))
        vtttextr = vtttext.get_rect()
        vtttextr.center = (500, 500)
        win.blit(vtttext, vtttextr)
        vttttext = reg.render(f'Pygame Minecraft', True, (0,0,0))
        vttttextr = vttttext.get_rect()
        vttttextr.center = (500, 100)
        win.blit(vttttext, vttttextr)
    pygame.display.update()
pygame.quit()
