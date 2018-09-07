# this is a program of hangman
# uses sql server, pygame, and images
# just for the fun, as a mission for a course
# V1.0
# PJ van Diepen 

import pygame
import pyodbc 
import random as ra
# from pygame.locals import * at the start of your program, you can omit pygame.

#kleuren
achtergrondkleur=(0,0,0)
tekstkleur=(0,128,0)

#posities teksten 
fonthoogte=36
offsetY=8
regelafstand=10

startpostekst1X=400
startpostekst2X=400
startpostekst3X=400
startpostekst4X=150
startpostekst5X=150

startpostekst1Y=5
startpostekst2Y=startpostekst1Y+fonthoogte+regelafstand
startpostekst3Y=startpostekst2Y+fonthoogte+regelafstand
startpostekst4Y=400
startpostekst5Y=startpostekst4Y+fonthoogte+regelafstand


clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((800,600)) 
screen.fill(achtergrondkleur)
font = pygame.font.SysFont("comicsansms", fonthoogte)
attempts=10
done = False


server = 'NLXXXX' 
database = 'hangman' 
username = 'hangman' 
password = 'hihangman' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

def StartGame():
    gewenste_lengte=ra.randint(3,8)
    cursor.execute("SELECT *  FROM Raad_Woord where len(woord)=?",gewenste_lengte)
    keuze_woorden=[]
    row = cursor.fetchone() 
    while row:
        keuze_woorden.append(row[1])
        row = cursor.fetchone() 
    random_woord=ra.choice(keuze_woorden)
    return  {'Sgewenste_lengte':gewenste_lengte, 'Srandom_woord':random_woord}


def update_galg(poging):
    attempts=poging
    plaatje=str(10-attempts)+'.jpg'
    te_lezen='C:\\Project\\hangmen_jpg\\'+plaatje
    img=pygame.image.load(te_lezen)
    screen.blit(img,(0,0))


def opnieuw():
    #parameters kleur, startpositie x,y en breedte hoogte
    #schoon gewonnen/verloren en start popnieuw vraag
    opnieuwf = font.render('Wil je nogmaals spelen? j/n',   True, (tekstkleur))
    screen.blit(opnieuwf,(startpostekst5X , startpostekst5Y))

def toon_welkom():
    welkomf = font.render('Welkom bij Galgje',   True, (tekstkleur))
    screen.blit(welkomf,        (startpostekst1X , startpostekst1Y))

def toon_lengte():
    lengte='lengte '+str(gewenste_lengte) 
    lengtef=font.render(lengte, True, (tekstkleur))
    pygame.draw.rect(screen, (achtergrondkleur),(startpostekst2X, startpostekst2Y, lengtef.get_width(),fonthoogte+offsetY))    
    screen.blit(lengtef,        (startpostekst2X, startpostekst2Y))


def toon_woord():
    # maak van de afzonderlijke karakters weer een string
    blanks="".join(word_guessed)
    blanksf=font.render(blanks, True, (tekstkleur))
    pygame.draw.rect(screen, (achtergrondkleur),(startpostekst3X, startpostekst3Y+offsetY, 400,fonthoogte+offsetY))
    screen.blit(blanksf,        (startpostekst3X, startpostekst3Y))

Startgamedict = StartGame()
random_woord = Startgamedict.get('Srandom_woord')
gewenste_lengte = Startgamedict.get('Sgewenste_lengte')
print(random_woord)
word_guessed = []
for letter in random_woord:
    word_guessed.append("-")

woord_geraden=False
toon_welkom() 
toon_lengte()
toon_woord()
update_galg(attempts)
player_guess = None

while not done:
    player_guess = None # will hold the players guess
    guessed_letters = [] # a list of letters guessed so far

 # create an unguessed, blank version of the word
    joined_word = None # joins the words in the list word_guessed
     
#    update_galg(attempts)
    for event in pygame.event.get():
           if event.type == pygame.QUIT:
               done = True
           if event.type == pygame.KEYDOWN:
               player_guess= (pygame.key.name(event.key))   
               print(player_guess)
               if woord_geraden==False:      
                   guessed_letters.append(player_guess)
                   if player_guess  in random_woord:
                     for letter in range(len(random_woord)):
                       if player_guess == random_woord[letter]:
                          word_guessed[letter] = player_guess
                          pygame.draw.rect(screen, (achtergrondkleur),(startpostekst3X, startpostekst3Y+offsetY, 300,fonthoogte+offsetY))
                          toon_woord()
                     if "-" not in word_guessed: # no blanks remaining
                       winstverlies='Gefeliciteerd '+random_woord+' was het woord'
                       winstverliesf = font.render(winstverlies,   True, (tekstkleur))
                       screen.blit(winstverliesf,(startpostekst4X , startpostekst4Y))
                       opnieuw()
                       woord_geraden=True
                       player_guess=''
                        
                   else:
                       attempts -= 1
                       update_galg(attempts)
                       if attempts==0:
#                           attempts=0
                           winstverliesf = font.render('Jammer, niet geraden',   True, (tekstkleur))
                           screen.blit(winstverliesf,(startpostekst4X ,startpostekst4Y))
# we doen alsof woord geraden is om nieuw spel te kunnen starten
                           opnieuw()    
                           woord_geraden=True
                           player_guess=''


           if woord_geraden and player_guess == 'n':
                   done=True
           elif woord_geraden and player_guess == 'j':
                   woord_geraden=False
                   player_guess=''
                   Startgamedict=StartGame()
                   random_woord=Startgamedict.get('Srandom_woord')
                   gewenste_lengte=Startgamedict.get('Sgewenste_lengte')
                   toon_lengte()
                   print(random_woord)
                   word_guessed = []
                   attempts = 10
                   update_galg(attempts)
                   for letter in random_woord:
                       word_guessed.append("-") 
                   toon_woord()    
                   pygame.draw.rect(screen, (achtergrondkleur),(startpostekst4X ,startpostekst4Y+offsetY, 800,fonthoogte+offsetY))
                   pygame.draw.rect(screen, (achtergrondkleur),(startpostekst5X ,startpostekst5Y+offsetY, 800,fonthoogte+offsetY))
    
    pygame.display.flip() # update the display
    clock.tick(60)
    

    
    
   