from gamelib import *

game = Game(1024,768,"Billy Bob And The Munster Uprising")
#Game graphics

#Background
bk = Animation("Background.jpg",2,game,4096/2,768)
game.setBackground(bk)

play = Image("play.png",game)
play.moveTo(1024/2,600)

htp = Image("How-To-Play.png",game)
htp.moveTo(play.x,play.y + 100)

Title1 = Image("Billy-Bob-and-The-.png",game)
Title1.moveTo(play.x,play.y - 400)
Title2 = Image("Munster-Uprising.png",game)
Title2.moveTo(play.x,play.y - 300)

Back = Image("Back.png",game)
Back.moveTo(100,700)

Next = Image("Next.png",game)
Next.moveTo(1024/2 + 400,768/2 + 350)

#Sound
Shoot = Sound("shoot.wav",1)

#Hero
Billy = Animation("Billy_Right.png",4,game,264/4,96)
Billy.moveTo(20,400)
Billy.resizeBy(20)

#Ground
ground = Image("ground.jpg",game)
ground.moveTo(Billy.x,660)


#Bullet
bullet = Image("bullet.png",game,use_alpha = False)
bullet.resizeBy(-85)
bullet.rotateBy(90,"right")
bullet.visible = False



#Monsters
Maggots = []
for index in range(30):
    Maggots.append(Animation("cave-maggot-giant.png",10,game,580/10,44,use_alpha = False))
    Maggots[index].resizeBy(50)
for index in range(30):
    x = randint(1024,5000)
    Maggots[index].moveTo(x,ground.y - 40)

Zombies = []
for index in range(30):
    Zombies.append(Animation("zombie_frame.png",4,game,136/4,96,use_alpha = False))
    Zombies[index].resizeBy(50)
for index in range(30):
    x = randint(1024,5000)
    Zombies[index].moveTo(x,ground.y - 75)

Ghosts = []
for index in range(30):
    Ghosts.append(Animation("ghost_frame.png",5,game,246/5,96,use_alpha = False))
    Ghosts[index].resizeBy(50)
for index in range(30):
    x = randint(1024,5000)
    Ghosts[index].moveTo(x,ground.y - 300)

    
#Title Screen
HowToPlay = False
while not game.over and HowToPlay == False:
    game.processInput()
    
    game.scrollBackground("left",2)
    Title1.draw()
    Title2.draw()


    ground.draw()
    play.draw()
         
    if play.collidedWith(mouse) and mouse.LeftClick:
        game.over = True
        
    game.update(30)
game.over = False
#How To Play
while not game.over:
    game.processInput()

    game.scrollBackground("left",2)
    
    ground.draw()

    game.drawText("A = Move Left",1024/2 - 100,768/2 )
    game.drawText("D = Move Right",1024/2 - 100,768/2 + 50)
    game.drawText("Left Click = Shoot",1024/2 - 100,768/2 + 100)

    Next.draw()

    if Next.collidedWith(mouse) and mouse.LeftClick:
        game.over = True
    
    game.update(30)
game.over = False

#Wave 1
wave1complete = 0
while not game.over:
    game.processInput()

    landed = False

    game.scrollBackground("left",2)
    
    ground.draw()
    bullet.move()
    Billy.draw()
    Billy.stop()
    
    if Billy.collidedWith(ground,"rectangle"):
        landed = True

    for times in range(100):
        ground.moveTo(Billy.x,660)
        
    for index in range(30):        
        if Maggots[index].x <= Billy.x:
            Maggots[index].setSpeed(3,270)
            Maggots[index].move()            
        if Maggots[index].x >= Billy.x:
            Maggots[index].setSpeed(3,90)
            Maggots[index].move()
            
        if Zombies[index].x <= Billy.x:
            Zombies[index].setSpeed(2,270)
            Zombies[index].move()
        if Zombies[index].x >= Billy.x:
            Zombies[index].setSpeed(3,90)
            Zombies[index].move()
    
        Ghosts[index].moveTowards(Billy,5)


        #Collision w/ Billy
        if Maggots[index].collidedWith(Billy):
            Billy.health -= 10
            Maggots[index].visible = False
            wave1complete += 1
        if Zombies[index].collidedWith(Billy):
            Billy.health -= 10
            Zombies[index].visible = False
            wave1complete += 1
        if Ghosts[index].collidedWith(Billy):
            Billy.health -= 10
            Ghosts[index].visible = False
            wave1complete += 1

        #Collision w/ bullet
        if Maggots[index].collidedWith(bullet):
            Maggots[index].visible = False
            bullet.visible = False
            wave1complete += 1
        if Zombies[index].collidedWith(bullet):
            Zombies[index].visible = False
            bullet.visible = False
            wave1complete += 1
        if Ghosts[index].collidedWith(bullet):
            Ghosts[index].visible = False
            bullet.visible = False
            wave1complete += 1

        if bullet.isOffScreen():
            bullet.visible = False
            
            
        if Billy.health == 0:
            game.over = True

         
    ##Controls
    if landed == False:
        Billy.y += 3           
    if keys.Pressed[K_d]:
        Billy.x += 10
        Billy.nextFrame()
    if keys.Pressed[K_a]:
        Billy.x -= 10        
        Billy.prevFrame()
    if keys.Pressed[K_SPACE]:
        Billy.y -= 20
        landed == False
    if mouse.LeftClick:
        Shoot.play()
        bullet.visible = True
        bullet.moveTo(Billy.x,Billy.y)
        bullet.moveTowards(mouse,100)


    game.drawText("Health: " + str(Billy.health),Billy.x - 50,Billy.y - 100)
    game.update(30)

    if wave1complete == 90:
        game.over = True
game.quit()
