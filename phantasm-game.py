import tkinter as tk
from tkinter import *
import pygame
from tkinter.ttk import *
from PIL import ImageTk, Image #importing Pillow library to manipulate images
import random, time
import random

pygame.init() #pygame initialization

windowMain = Tk()
windowMain.geometry("800x600")
windowMain.resizable(False, False)
windowIcon = PhotoImage(file = "lockLogo.png")#variable that stores Image
windowMain.iconphoto(False, windowIcon)#method that changes the window icon
windowMain.title("PHANTASM")

#Sounds
global mainScreenMusic
mainScreenMusic = "mainMusic.wav"
pygame.mixer.music.load(mainScreenMusic) #loads long audios into pygame music player and makes it playable
pygame.mixer.music.play(loops=-1)#makes the music loaded into mixer loop
click_sound = pygame.mixer.Sound("button_click.wav")#using pygame, makes a sound object that can be then played, stopped, etc
global sound_puzzle 
sound_puzzle = pygame.mixer.Sound("soundpuzzle.wav")
flip_sound = pygame.mixer.Sound("flip_sound.wav")

def exit_program():
    exit()

def clickTrack():
    print("Successful button click")#for our reference in the console

# Function to Start Level 1. 
def go_to_lvl1():
    #Switch from start screen to game screen
    pygame.mixer.music.stop() #stops the music module from playing the loaded file
    click_sound.play()#will play a button click sound after game mode is chosen

    windowMain.withdraw()  # Hide main window
    level1.deiconify()  # Show Level 1 window
# Level 1 Window
level1 = tk.Toplevel(windowMain)
level1.geometry("600x600")
level1.resizable(width=False, height=False)
level1.title("PHANTASM")
level1.withdraw()
windowIcon = PhotoImage(file = "lockLogo.png")
level1.iconphoto(False, windowIcon)
bg_lvl1 = tk.PhotoImage(file = "puzzle.png")

lvl_1 = tk.Label(level1, image = bg_lvl1)

lvl_1.pack()

hit = 0

mob = tk.PhotoImage(file = "SCARY.png")


def go_to_lvl2():
    click_sound.play()
    level1.withdraw()
    level2.deiconify()
    level2_UI()



def start():
        dropdown(level1)
        evil_Monster.pack()
        evil_Monster.place(relx=0.5, rely=0.5, anchor="center")
        evil_Monster.configure(height=70, width=70)
        button_startlvl1.destroy()
        

def hurt_SCARY(evil_Monster):
        global x_1
        global y_1
        global hit
        global button_endlvl1
        x_1 = random.randint(-280, 280)
        y_1 = random.randint(-280, 280)

        hit += 1

        if hit == 10:
            evil_Monster.destroy()
            button_endlvl1.configure(height= 4, width= 11)
            button_endlvl1.place(relx=0.5, rely=0.80, anchor="center")
            button_endlvl1.pack_forget()
            
            

        evil_Monster.place(x = x_1, y = y_1)
            
            
button_startlvl1 = tk.Button(level1, text= 'START', bg = 'grey', command=start)

button_startlvl1.pack()

button_startlvl1.configure(height= 4, width= 11)

button_startlvl1.place(relx=0.5, rely=0.80, anchor="center")

button_endlvl1 = tk.Button(lvl_1, text= 'Next level', bg = 'grey', command= go_to_lvl2)

button_endlvl1.pack_forget()

evil_Monster = tk.Button(level1, image = mob, command= lambda: hurt_SCARY(evil_Monster))

evil_Monster.pack_forget()          


        

global attempt
global matchNum #tracking matches
attempt=0
matchNum=0
# Triggers Level 2 window


# Level2, its logic and puzzle component
def level2_UI():
    global tarot_back_resized
    dropdown(level2)
    #Loaded the back image of the card
    card_back_image = Image.open("tarot_back.png")
    # Resized card back image
    tarot_back_resized = ImageTk.PhotoImage(card_back_image.resize((150, 180), Image.LANCZOS))
     # Iterating over the card_images dictionary and creating a new one with the same keys but resized values
    card_images = [
        ImageTk.PhotoImage(Image.open(f"easy_tarot{i}.png").resize((150, 180), Image.LANCZOS)) for i in range(2, 5)
    ]#card 2 card 3 card 4
    level2_logic(card_images)

flipped_cards = []#list for flipped cards(button, image)
# Function for Puzzle Level logic
def level2_logic(card_faces):
    global sound_puzzle, attempt, matchNum
    sound_puzzle = "soundpuzzle.wav"
    pygame.mixer.music.load(sound_puzzle)
    pygame.mixer.music.play(loops=-1)

    facesWPairs = card_faces * 2 #A list with dupes/pairs of the easy_tarot images
    random.shuffle(facesWPairs)

    cards = []#stores the card buttons, that have images on it
    for i, image in enumerate(facesWPairs):#i is index given through enumerate and image is temp var that holds each image from the list
        card = tk.Button(level2, image=tarot_back_resized, width=150, height=180, borderwidth=0, highlightthickness=0)
        card.config(command=lambda btn=card, img=image: flip_card(btn, img))#passes the card button as btn and image as img into the function
        card.place(x=(i % 3) * 155 + (180), y=(i // 3) * 210 + (80))
        cards.append(card)#keeping the buttons/cards from loss

     # Function to flip a card when button is pressed/triggered
    def flip_card(button, image):
        flip_sound.play()
        global attempt, flipped_cards

        if len(flipped_cards) < 2 and button["state"]=="normal":
            flip_sound.play()
            button.config(image=image)#configures the face image passed by facesWPairs
            flipped_cards.append((button, image))

        if len(flipped_cards)==2:
            level2.after(500, lambda: check_match())
            print("leaving flip card")

    # Function to check for a match
    def check_match():
        global attempt, matchNum
        if len(flipped_cards)==2:
            button1, card1_img = flipped_cards[0]  
            button2, card2_img = flipped_cards[1]

            if card1_img != card2_img:
                reset(button1, button2)
                attempt+=1
                if attempt>3:
                    show_game_over(level2)
            else:
                button1["state"] = "disabled"
                button2["state"] = "disabled"
                matchNum+=1
            
            flipped_cards.clear()

            if matchNum == 3 and attempt <= 3:
                show_proceed_button()


    def reset(button1, button2):
        button1.config(image=tarot_back_resized)
        button2.config(image=tarot_back_resized)
        button1["state"] = "normal"
        button2["state"] = "normal"


def show_game_over(yourLevel):
    pygame.mixer.music.stop()
    yourLevel.withdraw() 
    game_over_screen.deiconify()

# Restart(replay) button
def restart_game():
    pygame.mixer.music.stop()
    game_over_screen.withdraw()  # Close the game-over screen
    windowMain.deiconify()  # Show the main screen again

def show_proceed_button():#Proceed button for level 2
    proceed_button = tk.Button(level2, text="PROCEED", command=go_to_lvl3, font=("Sinister", 20, "bold"), bd=0, highlightthickness=0)
    proceed_button.place(relx=0.8, rely=0.9, anchor="center")  

def go_to_lvl3():
    pygame.mixer.music.stop()
    level2.withdraw()
    level3.deiconify()
    global canvas_level3, original, full_image
    canvas_level3 = tk.Canvas(level3, width=800, height=600, bg="black")
    canvas_level3.pack(fill="both", expand=True)
    full_image = load_resized_image("ladyonlight.png")  
    #original = canvas_level3.create_image(0, 0, image=full_image, anchor="nw")
    dropdown(level3)
    

#MAIN SCREEN
firstPageImg = Image.open("firstPage.png") #making sure the image is accessible
firstPageImg = firstPageImg.resize((800, 600), Image.LANCZOS)#Image.LANCZOS is from the Pillow Library. It reduces pixalation when resizing idk if we should use it

game_bg = ImageTk.PhotoImage(firstPageImg)#takes an image from Pillow library and converts tkinter image

canvas = Canvas(windowMain, width=800, height=600)#canvas widget adding
canvas.pack(fill=tk.BOTH, expand=True)

canvas.create_image(0, 0, anchor="nw", image=game_bg)
canvas.create_text(400, 110, text = "PHANTASM", font=("Fixedsys", 80))#adding text on top of canvas

canvas.create_text(400, 170, text = "Face your Nightmare:", font=("Fixedsys", 23))#adding text on top of canvas

#Buttons
ButtonImage = Image.open("startButton.png")#loading an image in pillow library to make an image object that can be worked with
ButtonImage = ButtonImage.resize((210, 105), Image.LANCZOS)
ButtonImage = ImageTk.PhotoImage(ButtonImage)#converts image to format working for tkinter(from PIL)/prep to use in tk
buttonStart = tk.Button(windowMain, image = ButtonImage, background="grey", command= go_to_lvl1)
buttonStart.image = ButtonImage #this button object will be referencing BI image object
canvas.create_window(400, 450, window = buttonStart)



# Level 2 Window
level2 = tk.Toplevel(windowMain)
level2.geometry("800x600")
level2.title("PHANTASM")
level2.withdraw()
level2.iconphoto(False, windowIcon)
#Level 2 Canvas
level2_bg = Image.open("puzzle.png") #making sure the image is accessible
level2_bg = level2_bg.resize((800, 600), Image.LANCZOS)

puzzle_bg = ImageTk.PhotoImage(level2_bg)#takes an image from Pillow library and converts tkinter image

level2_canvas = Canvas(level2, width=800, height=600)#canvas widget adding
level2_canvas.pack(fill=tk.BOTH, expand=True)

level2_canvas.create_image(0, 0, anchor="nw", image=puzzle_bg)

#Level3
level3 = tk.Toplevel(windowMain)
level3.title('PHANTASM')
level3.geometry("1000x1000")
level3.configure(bg="black")
level3.withdraw()

level3_canvas = Canvas(level3,width= 1000, height= 1000)
level3_canvas.pack(fill=tk.BOTH, expand=True)

def load_resized_image(img): 
    image = Image.open(img) #making sure the image is accessible
    image = image.resize((1000, 1000), Image.LANCZOS)
    canvas_image = ImageTk.PhotoImage(image)#takes an image from Pillow library and converts tkinter image
    return canvas_image

# Original image, resized using subsample
full_image = load_resized_image('ladyonlight.png')
full_image.image = full_image  
original = level3_canvas.create_image(0, 0, image=full_image, anchor="nw")



#full_image = tk.PhotoImage(file='CS1010-Project/ladyonlight.png')
#original = canvas.create_image(0, 0, image=full_image, anchor="nw")

L1 = tk.Label(level3, text="Phantasm Level 3", bg="black", fg="grey",font=("courier",7),height = 1, width=15)
L1.place(x=4, y=5)

text1=("you wander around, looking for an answer, an explanation as to what is going on. On an empty street, you encounter a mysterious woman.\n"
       "Her face is featureless. She has no eye sockets, lips or any features. However, her presence doesn't feel alarming or unsafe.\n"
       "You hear her faint whispers, ”confront or be consumed” ring through your mind. It seems important, but what could it mean?\n")
L2 = tk.Label(level3, text=text1, bg="grey", fg="black",font=("courier",7))
L2.place(x=150, y=5)


text2=("as you wander explore around, trying to decipher the womans message, you see a strange creature climbing the roof\n"
       "It seems to be on all fours,like nothing you've seen before. You start to make a run for it but…")


text3=("You encounter a nightmare in creature form, you seem to be trapped, with no where left to go. You cant run, you cant hide, your attacks are ineffective.\n" 
       "The whispers and voices call out to you, they distract your mind from forming any thoughts. you stand still.\n"
        "Frozen. Only hearing voices, getting flashbacks of what seems to be a previous live, and feeling overwhelmed and confused. Theres only one thing left to do:")


text4=("You gather the courage to confront this nightmare of a creature. Your bravery has weakened the creature that fuels its strength through your fears.\n"
       "Through continuous demonstrations of courage, the creature weakens, the voices start to fade, and the creature disappears.\n")
text5=("Your mind feels foggy. And you slowly drift to a sleeping state")

text6=("you wake up feeling dizzy. You realize you are at the same parking lot from where you first remember getting an eerie sensation. [SUBJECT TO CHANGE]\n"
       "it seems like you fell asleep inside of your car. Someone comes up and knocks. You roll down your window to hear “Hey man you've been here for a while now, do you need anything?”\n" 
       "Right then and there you realize it was all a dream, none of it was real you are now safe, but this event has forever changed your life. ")

text7= ("Overwhelmed by fear, you can only think of running. You attempt to flee but the creature towers over you at 15 feet tall, catching up with just a single step.\n"
        "It's cold claws grip your head, and thats your last memory before you awaken.")

text8= ("You awake in a strange set of mind, the walls of the room you are in are closing in and the air stinks of rot and decay.\n"
        "The whispers you once heard are now screams. You get flashbacks to memories, nightmares, regrets and sorrows. You seek a way out but every door leads to the same room.\n"
        "the walls seem to close in tighter every second.You are doomed to the horrors of your own mind, trapped, endlessly relieving every tragedy.")
text9=("Thank you for Playing! You sucessfully ended the game! :)")
text10=("Thank you for playing! You unsucessfully ended the game :(")
#L1_window = canvas.create_window(200, 50, window=L1)

def changeBackground1():
    newBackground = load_resized_image('guyonroof.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text2)

def changeBackground2():
    newBackground = load_resized_image('nightmarecreature.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text3)
    
def changeBackground3():
    newBackground = load_resized_image('nightmarecreature.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text4)

def changeBackground4():
    newBackground = load_resized_image('transitiontoending.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text5)

def changeBackground5():
    newBackground = load_resized_image('carinterior.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text6)

def changeBackground6():
    newBackground = load_resized_image('nightmarecreature.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text7)

def changeBackground7():
    newBackground = load_resized_image('badending.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text8)

def changeBackground8():
    newBackground = load_resized_image('endscreen.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text9)

def changeBackground9():
    newBackground = load_resized_image('endscreen.png')
    level3_canvas.itemconfig(original, image=newBackground)
    level3_canvas.image = newBackground
    L2.config(text=text10)

# here, counter will check the times the button has been clicked, this will change the backgrounds along with the text
count = 0
def next_step():
    global count
    if count == 0:
        changeBackground1()
        count += 1
        button_1.config(text="Next ", command=next_step)
    #elif count == 1:
       # changeBackground2()
       # count += 1
       # button_1.config(text="Next ", command=next_step)
    elif count == 1:
        changeBackground2()
        count += 1
        button_1.config(text="Next ", command=next_step)
    elif count == 2:
        changeBackground3()
        count += 1
        button_1.config(text="Next ", command=next_step)
    elif count == 3:
        changeBackground5()
        count += 1
        button_1.config(text="Next ", command=next_step)
    #elif count == 4:
        #changeBackground6()
        #count += 1
        #button_1.config(text="Next ", command=next_step)
    elif count == 4:
        changeBackground9()
        count += 1
        button_1.config(text="Exit ", command=exit_program)
    elif count == 5:  #3 was changed to 2
        button_1.pack_forget()
    


button_1 = tk.Button(level3, text="Next", command=next_step, width=19, height=2, bg="black", fg="red", font=("courier"))
button_1.place(x=555, y=530)

#this makes the buttons that will both have different outputs appear


#button_1 = tk.Button(window, text="Next", command=next_step, width= 19, height= 2,bg="black", fg= "red",font=("courier"))
#button_1.place(x=555, y=530,)

#button_successend = tk.Button(window, text="Confront Nightmare", command=successful_ending)
#button_successend.place(x=555,y=530)#change
#button_unsuccessend = tk.Button(window, text="Attempt to Flee", command=unsuccessful_ending)
#button_unsuccessend.place(x=555,y=530) # change

# Game over window
game_over_screen = tk.Toplevel()
game_over_screen.geometry("800x600")
game_over_screen.resizable(False, False)
game_over_screen.title("PHANTASM")
game_over_screen.withdraw()
game_over_image = Image.open("gameoverscreen.png").resize((800, 600), Image.LANCZOS)
game_over_tk_image = ImageTk.PhotoImage(game_over_image)
    
# game over canvas
game_over_canvas = Canvas(game_over_screen, width=800, height=600)
game_over_canvas.pack(fill=tk.BOTH, expand=True)
game_over_canvas.create_image(0, 0, anchor="nw", image=game_over_tk_image)
game_over_canvas.image = game_over_tk_image #referencing the image that it is itself to avoid loss

#Restart Button
restartImage = Image.open("restartButton.png")
restartImage = restartImage.resize((140, 90), Image.LANCZOS)
restartImage = ImageTk.PhotoImage(restartImage)
restart_button = tk.Button(game_over_screen, image=restartImage, command=restart_game)
restart_button.place(relx=0.5, rely=0.65, anchor="center")

#Pause window
#pause 

#Dropdown menu for quit and main menu. use it for your levels
def dropdown(yourLevel):
    menu_bar = tk.Menu(yourLevel)
    game_menu = tk.Menu(menu_bar, tearoff=0)
    game_menu.add_command(label="MAIN MENU", command=lambda: show_home(yourLevel))
    game_menu.add_command(label="PAUSE", command=lambda: show_pause(yourLevel))
    game_menu.add_command(label="QUIT", command=yourLevel.quit)
    menu_bar.add_cascade(label="MENU", menu=game_menu)
    yourLevel.config(menu=menu_bar)
def show_home(currentLevel):
    global mainScreenMusic
    currentLevel.withdraw()
    pygame.mixer.music.stop()
    pygame.mixer.music.load(mainScreenMusic)
    pygame.mixer.music.play(loops=-1)
    windowMain.deiconify()
def show_pause(currentLevel):# i want to hide this level but remember to show it after resume button is hit
    currentLevel.withdraw()
    pygame.mixer.music.stop()
    #pause.deiconify()
dropdown(windowMain)
windowMain.mainloop()