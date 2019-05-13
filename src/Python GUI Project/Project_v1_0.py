import PIL
import os
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random


PATH = './Resources/'
DICE = ['d20', 'd12', 'd10', 'd8', 'd6', 'd4']
OFFSET = 64
labelfont=('times', 18, 'bold')
bgColor="cornflower blue"

class Window(Frame):

    def __init__(self, master=None):
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()
        
    def init_window(self):
        #set title here
        self.master.title("Dice Roller 1.0")
        self.configure(background = "DodgerBlue4")
        #window icon
        self.master.wm_iconbitmap(PATH+'dice_rolling.ico')
        #fill space of root
        self.pack(fill=BOTH, expand=1)

        #--------------------------File Menu-------------------------------#
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = Menu(menubar, tearoff=0)
        submenu = Menu(fileMenu, tearoff=0)
        submenu.add_command(label="Roll History", command= self.showHistory, underline = 0)
        submenu.add_command(label="Clear history", command= self.clearHistory, underline = 0)
        fileMenu.add_cascade(label="History", menu=submenu, underline = 0)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.onExit, underline = 0)
        menubar.add_cascade(label="Menu", menu=fileMenu)

        #----------------------Buttons and Labels--------------------------#
        bottomFrame = Frame(self.master, background = "DodgerBlue4")
        bottomFrame.pack(side = "bottom", fill = X)

        #create roll button
        self.create_button(bottomFrame)
        
        #create roll results/total label
        self.create_roll_results(bottomFrame)
        #self.totals_label(bottomFrame)
        #Quantity of dice to roll
        self.dice_quant(bottomFrame)

        #show images of the dice and radio buttons
        imgSpace = 0
        i = 1
        for die in DICE:
            self.showImg(die, imgSpace, i)
            ##self.showRadio(die, imgSpace, i)
            imgSpace += OFFSET
            i += 1

    #-----------------------Methods------------------------#
    #select number of dice using spinbox
    def dice_quant(self, frame):
        quantity = Spinbox(frame, textvariable = q,
                           font=('times', 18, 'bold'),
                           increment=1, from_= 1, to = 10, width= 5, 
                           wrap = True, fg="White", bg=bgColor,
                           buttonbackground= "steel blue", justify=CENTER).pack(side = 'top', anchor = E)
    #results/totals label
    def create_roll_results(self, frame):
        results = Label(frame, textvariable = s, 
                        anchor=W, justify=CENTER,
                        font=labelfont,
                        fg="White",
                        background = bgColor, bd=1,
                        relief = GROOVE).pack(side = 'bottom', anchor = SE)

    #roll button 
    def create_button(self, frame):
        rollBtn = Button(frame, compound='center', text="ROLL!",
                         font=labelfont, 
                         fg="White", bg = bgColor,
                         bd = 2, relief = RAISED,
                         command=self.num_Rolls)
        image = ImageTk.PhotoImage(file=PATH+"DiceRolling.png")
        #image = ImageTk.PhotoImage(file=PATH+"roll_dice.png")
        rollBtn.config(image=image)
        rollBtn.image = image
        rollBtn.pack(side = 'left', anchor = NW)
      
    #show the Dice    
    def showImg(self, die, offset,i):
        die = die+'.png'        
        load = Image.open(PATH + die)
        load = load.convert("RGBA")
        render = ImageTk.PhotoImage(load)

        #radio buttons with no dots
        img = Radiobutton(self, image=render, 
                          background = "cornflower blue",
                          variable = d, value = i,
                          padx = 2, indicatoron = 0,bd=1,
                          selectcolor= "steel blue")
        img.image = render
        img.place(x = offset, y = 0)
        #print(load.format, load.size, load.mode)

    def num_Rolls(self):
        total = 0
        if (int(q.get()) == 1):
            roll = self.roll_dice()
            self.get_values(roll)
        if(int(q.get()) > 1):
            for i in range(1, int(q.get())+1):
                roll = self.roll_dice()
                total += roll
            self.get_values(total)

    def get_values(self,total):
        if d.get() == 1:
            s.set(str(q.get()) +DICE[0] +": " + str(total))
            self.print_values(total, DICE[0])
        if d.get() == 2:
            s.set(str(q.get()) +DICE[1] +": " + str(total))
            self.print_values(total, DICE[1])
        if d.get() == 3:
            s.set(str(q.get()) +DICE[2] +": " + str(total))
            self.print_values(total, DICE[2])
        if d.get() == 4:
            s.set(str(q.get()) +DICE[3] +": " + str(total))
            self.print_values(total, DICE[3])
        if d.get() == 5:
            s.set(str(q.get()) +DICE[4] +": " + str(total))
            self.print_values(total, DICE[4])
        if d.get() == 6:
            s.set(str(q.get()) +DICE[5] +": " + str(total)) 
            self.print_values(total, DICE[5])

    #roll dice method
    ##add load_list call for each die, and pass in the name of each die or use d
    def roll_dice(self):
        if d.get() == 1:
            r = random.randint(1, 20)
            self.load_list(history, r)
            return r
        if d.get() == 2:
            r = random.randint(1, 12)
            self.load_list(history, r)
            return r
        if d.get() == 3:
            r = random.randint(1, 10)
            self.load_list(history, r)
            return r
        if d.get() == 4:
            r = random.randint(1, 8)
            self.load_list(history, r)
            return r
        if d.get() == 5:
            r = random.randint(1, 6)
            self.load_list(history, r)
            return r
        if d.get() == 6:
            r = random.randint(1, 4)
            self.load_list(history, r)
            return r

    def onExit(self):
        self.master.destroy()

    def print_values(self, total, die):
        print("\nRoll history: ")
        text_file = open("roll_history.txt", 'a')
        text_file.write("Roll History: \n")
        #iterate through all keys and values of history dict
        print("{0}{1}: {2} Total:{3}".format(str(q.get()), die, history[die], total)) #printing to console (for debugging)
        #write out to a file the history of the rolls
        ##with open("roll_history.txt", 'a') as text_file:
        print("{0}{1}: {2} Total:{3}".format(str(q.get()), die, history[die], total), file= text_file) #different format for printing
        text_file.write('\n')
        text_file.close
        for vals in history.values():
            vals.clear()

    def showHistory(self): 
        os.system('roll_history.txt')

    def clearHistory(self):
        with open("roll_history.txt", 'w') as txtfile:
            txtfile.write("")

    def load_list(self, history, value):
        for i in range(1,7):
            if(d.get() == i):
                k = str(DICE[i-1])
                history[k].append(value)

#create root
root = Tk()

d = IntVar()
s= StringVar()
#t = StringVar()
q = StringVar()
s.set("Select A Die")
d.set(1)


keys = DICE
history = {key: [] for key in keys}
        
w = 385 # width for the Tk root
h = 185 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

#configuration of main window
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.resizable(width = False, height = False)

#creating instance of window
prgm = Window(root)

prgm.pack()

#mainloop
root.mainloop()

