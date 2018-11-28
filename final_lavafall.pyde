add_library('sound')
import os, random, time
path = os.getcwd()
gravConstant = 35 # gravity constant bec most values have to be altered by this number
gravLine = 100 #distance of gravity line from screen edge
nameD=""
#name=""


class Game:
    def __init__(self):
        self.w=1500
        self.h=700
        self.g1=100
        self.g2=600
        self.x=0
        self.character="bear"
        self.hero = Hero(50,self.g2-gravConstant,self.g1,self.g2,38,77,100,7,self.character+'Run.png')
        self.st='menu'
        self.pause=False
        self.loadGraphics()
        self.imgS=loadImage(path+"/menu.png")
        self.imgC=loadImage(path+"/pickch.png")
        self.imgB=loadImage(path+"/layer1.png")
        self.imgLand=loadImage(path+"/layer2.png")
        self.imgRoof=loadImage(path+"/layer3.png")
        self.imgN=loadImage(path+"/name.png")
        self.name=""
        self.gameOverImg = loadImage(path+'/gameOver.png')
        self.pauseImg= loadImage(path + "/paused.png")
        self.winImg=loadImage(path + "/win.png")
        #self.allsound=SoundFile(this,path+'/music.mp3')

        
        
    def loadGraphics(self):
        self.lava=[]
        self.coins=[]
        self.rocks=[]
        self.land=[]
        self.roof=[]
        self.flag = []
                
        f = open(path+"/lavafall.csv","r")
        for obj in f:
            obj = obj.strip().split(",")
            if obj[0] == "lava2":
                self.lava.append(Lavafloor(int(obj[1]),int(obj[2]),int(obj[3]),int(obj[4]),obj[5]))
            elif obj[0] == "lava":
                self.lava.append(Lavafloor(int(obj[1]),int(obj[2]),int(obj[3]),int(obj[4]),obj[5]))
            elif obj[0] == "layer2":
                self.land.append(Land(int(obj[1]),int(obj[2]),int(obj[3]),int(obj[4]),obj[5]))
            elif obj[0] == "layer3":
                self.roof.append(Land(int(obj[1]),int(obj[2]),int(obj[3]),int(obj[4]),obj[5]))
            elif (obj[0] == "blueCoin") or (obj[0] == "redCoin") or (obj[0] == "goldCoin") or (obj[0] == "blueDimond") or (obj[0] == "redDimond"):
                self.coins.append(Coin(int(obj[1]),int(obj[2]),int(obj[3]),int(obj[4]),int(obj[5]),int(obj[6]), obj[7]))
            elif (obj[0] == "smallRock") or (obj[0] == "mediumRock") or (obj[0] == "bigRock"):
                self.rocks.append(Rock(int(obj[1]),int(obj[2]),int(obj[3]),int(obj[4]),int(obj[5]), obj[6]))
            elif obj[0] == 'flag':
                self.flag.append(Flag(int(obj[1]),int(obj[2]),int(obj[3]),int(obj[4]),obj[5]))
        f.close()
        
    def display(self):
        
        if self.st == "menu":
            background(self.imgS)
            
        elif self.st == "changeCharacters":
            #loading an image with 4 characters that I'll pick
             background(self.imgC)
                
        elif self.st == "play": 
            
            #self.allsound.play() 
            
            # background(self.imgB)
            image(self.imgB,0,0,self.w-game.x%self.w,self.h,game.x%self.w,0,self.w,self.h)
            image(self.imgB,self.w-game.x%self.w,0,game.x%self.w,self.h,0,0,game.x%self.w,self.h)
            
            
                    
            for lava in self.lava:
                lava.display()
            
            for land in self.land:
                land.display()
            
            for roof in self.roof:
                roof.display()
            
            for rock in self.rocks:
                rock.display()
            
            for coin in self.coins:
                coin.display()
            
            for flag in self.flag:
                flag.display()
                
            self.hero.display()
            
            
            try:
                f = open("scores.csv","r") 
                for l in f:
                    nameD=l.strip().strip(",")
                f.close()
                if nameD.isdigit() or "," in nameD:
                    textSize(32)
                    text("Score: "+ str(self.hero.coinNum), 50, 30)
                else:
                    textSize(32)
                    text(str(nameD)+"'s score: "+ str(self.hero.coinNum), 50, 30)  
            except:
                textSize(32)
                text("Score: "+ str(self.hero.coinNum), 50, 30)
            
                
        elif self.st == "name":
            background(self.imgN)
            text("Please enter your name:", 100,100)
            text(game.name, 100, 200) #empty string at start - keypressed function adds to the string
                

class Creature:
    def __init__(self,x,y,g1,g2,r,w,h,F,img):
        self.x=x
        self.y=y
        self.g1=g1
        self.g2=g2
        self.r=r
        self.w=w
        self.h=h
        self.F=F
        self.f = 0
        self.vx = 0
        self.vy = 0
        self.dir = 1 #by default it is straight up
        self.img=loadImage(path+'/'+img)
        
    def update(self):
        pass
    
    def display(self):
        self.update()
        self.hero.display()

class Hero(Creature):
    def __init__(self,x,y,g1,g2,r,w,h,F,img):
        Creature.__init__(self,x,y,g1,g2,r,w,h,F,img)
        self.keyHandler = {UP:False,DOWN:False}
        self.gameOver = 0
        self.vx = 4
        self.vy=0
        self.antigravity = False
        self.coinNum = 0
        self.win=False

        
    def painfulCollision(self): #function works for lava. 
        for lava in game.lava:
            if (lava.x<=self.x<=lava.x+lava.w and self.y+gravConstant == lava.y) or \
                (lava.x<=self.x<=lava.x+lava.w and self.y-gravConstant == lava.y+gravLine):
                    self.death()
                    break
            
        for rock in game.rocks:
            if self.distance(rock)<self.r+rock.r//2: #account for lost radius of image
                self.death()
                break
        
        for coin in game.coins:
            if self.distance(coin)<self.r+coin.w//2:
                self.coinNum=self.coinNum + coin.v
                game.coins.remove(coin)
                del coin
        
        for flag in game.flag:
            if self.x >= flag.x:
                self.win=True
                time.sleep(2)
                game.__init__()
                
    
    def death(self):
        self.antigravity = False
        self.gameOver = 90
        print "dead"
        self.keyHandler[UP]=False
        self.F = 6
        self.w = 89
        self.r = 45
        self.vy = 3
        self.img = loadImage(path+'/'+game.character+'Die.png')
        
    def distance(self,object):
        return((object.x-self.x)**2 + (object.y-self.y)**2)**0.5
        
    def gravity(self):
        if self.gameOver>0:
            self.vx=0
            return
        
        if self.antigravity == True:
            if self.y == self.g1+gravConstant:
                self.vy=0
        if self.antigravity == False:
            if self.y+gravConstant == self.g2:
                self.vy=0
        
    def update(self):
        
        self.x+=self.vx
        self.y+=self.vy
        
        print self.vy
        self.gravity()
        
        if self.gameOver >0:
            self.vy+=0.0001
            return
        
        if self.gameOver==0:
            self.painfulCollision()
            
        #move to G1
            if self.keyHandler[UP]:
                self.antigravity = True
                self.vy=-10
                self.dir=-1
                self.gravity()
        #move to G2
            elif self.keyHandler[DOWN]:
                self.antigravity = False
                self.vy=10
                self.dir=1
                self.gravity()
        
        if self.x>=game.w//2:
            game.x+=self.vx
        
    def display(self):
        if self.gameOver > 1:
            self.gameOver -= 1
        elif self.gameOver == 1: #and win
            time.sleep(2)
            f = open("scores.csv","a") #add scores to CSV
            f.write(str(game.hero.coinNum) + "\n")
            f.close()
            game.__init__()
        
        self.update()
        
        stroke(0,255,0)
        line(self.x-self.r-game.x,self.g1,self.x+self.r-game.x,self.g1)
        line(self.x-self.r-game.x,self.g2,self.x+self.r-game.x,self.g2)
        
        self.f = (self.f+0.1)%self.F
        
        if self.dir>0:
            image(self.img,self.x-self.r-game.x,self.y-self.r-10,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-self.r-game.x,self.y-self.r-10,self.w,self.h,int(self.f)*self.w,self.h,int(self.f+1)*self.w,0)
            

        
class Lavafloor: #img
    def __init__(self,x,y,w,h,img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img=loadImage(path+'/'+img)
    
    def display(self):
        image(self.img,self.x-game.x,self.y,self.w,self.h)

class Coin:
    def __init__(self,x,y,w,h,F,v,img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.F=F
        self.f=0
        self.v=v
        self.img=loadImage(path+'/'+img)

    
    def display(self):
        self.f = (self.f+0.12)%self.F
        image(self.img,self.x-game.x,self.y, self.w, self.h, int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)

class Rock:
    def __init__(self,x,y,w,h,r,img): #img
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.r=r
        self.img=loadImage(path+'/'+img)
    
    def display(self):
        image(self.img, self.x-game.x, self.y, self.w, self.h)

class Land:
    def __init__(self,x,y,w,h,img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img = loadImage(path+'/'+img)
    
    def display(self):
        image(self.img,self.x-game.x,self.y,self.w,self.h,0,0,self.w,self.h)

class Flag:
    def __init__(self,x,y,w,h,img):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.img = loadImage(path+'/'+img)
    
    def display(self):
        image(self.img,self.x-game.x,self.y,self.w,self.h,0,0,self.w,self.h)
    
game = Game()
        
def setup():
    size(game.w,game.h)
    stroke(255)
    background(0)

def draw():
        
    if not game.pause:
        background(0)
        game.display()
    else:
        image(game.pauseImg,game.w//2-200,game.h//2-100)
        
    if game.hero.gameOver == 1:
        image(game.gameOverImg,game.w//2-500,game.h//2-200)    
        
    if game.hero.win==True:
        image(game.winImg,game.w//2-500,game.h//2-200)
        
def keyPressed():
    if keyCode == UP:
        game.hero.keyHandler[UP] = True
        game.hero.keyHandler[DOWN] = False
        
    if keyCode ==DOWN:
        game.hero.keyHandler[DOWN] = True
        game.hero.keyHandler[UP] = False
        
    if key == 'p':
        game.pause = not game.pause
        
    if game.st=='name':
        if 'a' <= key <= 'z' or 'A' <= key <= 'Z' or keyCode == 32:
            game.name+=key
        elif keyCode == 8:  
            game.name=game.name[:len(game.name)-1]
        elif keyCode == 10:
            nameD=game.name
            f = open("scores.csv","a") #add scores to CSV
            f.write("{0},".format(game.name))
            f.close()
            game.__init__()
            
        
def mouseClicked():
    print game.st
    
    if game.st == 'menu':
        if game.w//3 <= mouseX <= (game.w//3)*2 and 0 <= mouseY <= game.h//3:
            game.st="play"
            nameD=game.name
        
        elif game.w//3 <= mouseX <= (game.w//3)*2 and game.h//3 <= mouseY <= (game.h//3)*2:
            game.st="changeCharacters"
            
        elif game.w//3 <= mouseX <= (game.w//3)*2 and  (game.h//3)*2 <= mouseY <= game.h:
            game.st="name"
    
    elif game.st=="changeCharacters":
        
        if 0 <= mouseX <= game.w//3 and  0 <= mouseY <= game.h-100:
            game.character="bear"
            game.st='menu'
            game.hero = Hero(50,game.g2-gravConstant,game.g1,game.g2,38,77,100,7,game.character+'Run.png')
            
        elif game.w//3 <= mouseX <= 2*(game.w//3) and 0 <= mouseY <= game.h-100:
            game.character="fox"
            game.st='menu'
            game.hero = Hero(50,game.g2-gravConstant,game.g1,game.g2,38,77,100,7,game.character+'Run.png')
            
        elif 2*(game.w//3) <= mouseX <= game.w and 0 <= mouseY <= game.h-100:
            game.character="monkey"
            game.st='menu'
            game.hero = Hero(50,game.g2-gravConstant,game.g1,game.g2,38,77,100,7,game.character+'Run.png')
            
            
            
          