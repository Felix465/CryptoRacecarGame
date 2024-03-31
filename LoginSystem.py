import pygame, sys

import mysql.connector
import re
from raceGame import *
from twilio.rest import Client


currentUser = None

system = []
mydb = mysql.connector.connect(
    host="77.68.35.85",
    user="y13felix",
    password="x6J5de_13",
    database="y13felix"

)


def extractDB():

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM users")

    myresult = mycursor.fetchall()

    table = []
    for i in myresult:
        table.append(i)

    x = list(map(Users, table))# adds the users to the class


    return x



def isValidP(number):
    validPhone = r"^([+]{1}[0-9]{1,3})[0-9]{7,12}$"
    #maximum length of a phone number is 15 digits 3 + 12
    print(number)
    x = re.match(validPhone, number)

    print(x)
    if x is not None:
        print('match succsess')
        return True
    else:
        return False

MakeUserReturn = '' # what the pop ups should appear in the make user screen
#timer = 0
def MakeUser():
    global MakeUserReturn
    global UserList
    global timer
    global currentUser
    global code
    timer = 0
    newUser = choose_username.GetMessage()
    newPass = choose_password.GetMessage()
    newPass = XORcipher(newPass)
    newPhone = choose_phone.GetMessage()
    guess = code_guess.GetMessage()
    sleep(1)
    try:
        guess = int(guess)
    except:
        pass
    for users in UserList:
        if users.GetName() == newUser:
            MakeUserReturn = 'Username Exists'
            print(users.GetName())
            print(users.GetID())#checks to see if the username already exists
            return MakeUserReturn
    if len(choose_password.GetMessage()) <5:
        timer = 0
        MakeUserReturn = 'Password Invalid'
        return MakeUserReturn#pasword must be greater than 5
    if isValidP(newPhone):
        if 'code' in globals():

            if guess == code:
                x = Users([0,newUser,newPass, newPhone,50,0, 0,0,200])#passes 0 as user id temporarly
                print('great')
                x.addToDB()
                UserList = extractDB()
                currentUser = x#if the user has a valid password username and the code is correct only then is a user created
                MakeUserReturn = 'Create User'
            else:
                print(code)
                print(guess)
                MakeUserReturn = 'Enter Code'
        else:
            MakeUserReturn = 'Enter Code'



    else:
        MakeUserReturn = 'Phone number invalid'
        return MakeUserReturn



#code = 0
def SendCreate():
    global MakeUserReturn
    global timer
    timer = 0
    newPhone = choose_phone.GetMessage()
    if isValidP(newPhone):
        SendSMS(newPhone)
    else:
        MakeUserReturn = 'Failed Send'

def SendSMS(num):
    global code
    global timer
    global MakeUserReturn
    timer = 0
    sleep(1)

    MakeUserReturn = ''
    account_number = 'AC784562f46e83189f98d17ad7afaf3cd6'
    auth_token = '1127e4301ae7fdaecde5ead8be9b7b41'

    twilio_number = '+16813846323'
    target_number = f'{num}'

    client = Client(account_number, auth_token)
    code = random.randint(10000,99999)
    try:

        message = client.messages.create(body=f"{code}", from_=twilio_number, to=target_number)#responsible for sending a message, twilio docs

        MakeUserReturn = 'Code Sent'
    except:
        MakeUserReturn = 'Failed Send'



def createUserPage():
    global system
    global timer
    sleep(1)




    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            choose_username.IsActive(event)
            choose_username.IsTyping(event)
            choose_password.IsActive(event)
            choose_password.IsTyping(event)
            choose_phone.IsActive(event)
            choose_phone.IsTyping(event)
            code_guess.IsActive(event)
            code_guess.IsTyping(event)

        screen.fill((255,255,255))

        choose_username.ActiveFalse()
        choose_username.EverythingElseLoop()
        choose_password.ActiveFalse()
        choose_password.EverythingElseLoop()
        choose_phone.ActiveFalse()
        choose_phone.EverythingElseLoop()
        code_guess.ActiveFalse()
        code_guess.EverythingElseLoop()

        button("Create", 325, 505, 100, 50, MakeUser)
        button("Send Code", 300, 430, 150, 50, SendCreate)
        #diffrent pop ups below

        if 'timer' in globals():
            timer += 1
            if timer <= 500 and MakeUserReturn == 'Username Exists':
                popUp('Username In Use', (235, 21, 14), screen)

            if timer <= 500 and MakeUserReturn == 'Password Invalid':
                popUp('Password too short', (235, 21, 14), screen)

            if timer <= 500 and MakeUserReturn == 'Phone number invalid':
                popUp('Phone number invalid', (235, 21, 14), screen)

            if timer <= 500 and MakeUserReturn == 'Enter Code':
                popUp('Code Incorrect', (235, 21, 14), screen)
            if timer <= 500 and MakeUserReturn == 'Failed Send':
                popUp('Could not send code', (235, 21, 14), screen)

            if timer <= 500 and MakeUserReturn == 'Code Sent':
                popUp('Code Sent', (26, 199, 4), screen)

            if timer <= 500 and MakeUserReturn == 'Create User':
                popUp('User Created', (26, 199, 4), screen)
                if timer == 200:
                    setUser(currentUser)
                    game_intro()#calls the next part of the program



        pygame.display.flip()
        clock.tick(60)




def XORcipher(text):
    if len(text) >0:
        a = ''.join(bin(ord(c)) for c in text).replace('b', '') # turn to binary
        x = int(a, 2) # turn to number
        y = ''
        for i in text:
            y += '11110011' # key used
        y = int(y, 2)# turn to number
        print(x)
        print(y)
        print(x ^ y)
        return (x^y)
    else:
        return 0#if a password of nothing is entered when they guess the password

def login():
    global currentUser
    global even
    global popUpType
    userNameGuess = username.GetMessage()
    print(userNameGuess)
    passwordGuess = password.GetMessage()
    passwordGuess = XORcipher(passwordGuess)



    for i in UserList:
        if i.GetName() == userNameGuess:
            print("match")
            if i.GetPassword() == str(passwordGuess):
                currentUser = i
                print(f"logged in as {currentUser.GetName()}")#if username and password match
                popUpType = 'success'
                even = 0

                return True



            else:

                even = 0
                popUpType = 'PasswordIncorrect'
                return False
    even = 0
    popUpType = 'UsernameIncorrect'








class Users:
    def __init__(self, array):
        self.__UserId = array[0]# all users in database would be transformed into user objects and compared using the user class
        self.__Name = array[1]
        self.__Password = array[2]
        self.__Phone = array[3]
        self.__Currency = array[4]
        self.__Highscore = array[5]
        self.__Red = array[6]
        self.__Green = array[7]
        self.__Blue = array[8]


    ####GETTERS
    def GetID(self):
        return self.__UserId
    def GetColour(self):
        colour = (self.__Red, self.__Green, self.__Blue)
        return colour

    def GetName(self):
        return self.__Name
    def GetPassword(self):
        return self.__Password
    def GetPhone(self):
        return self.__Phone
    def GetCurrency(self):
        return self.__Currency
    def GetHighscore(self):
        return self.__Highscore
    #####
    def SetPassword(self, new):
        self.__Password = new
        self.UpdateDatabase()

    def SetColour(self, c):
        self.__Red = c[0]
        self.__Green = c[1]
        self.__Blue = c[2]
        self.UpdateDatabase()

    def SetHighscore(self, new):
        self.__Highscore = new
        self.UpdateDatabase()


    def setCurrency(self, new):
        mycursor = mydb.cursor()
        self.__Currency = new

        sql = f"UPDATE users SET ingame_currency = '{self.__Currency}' WHERE user_name = '{self.__Name}'"

        mycursor.execute(sql)

        mydb.commit()
    def tempSetCurrency(self, new):
        self.__Currency = new

    def UpdateDatabase(self):
        mycursor = mydb.cursor()

        sql = f"UPDATE users SET password = '{self.__Password}', Phone_number = '{self.__Phone}',ingame_currency = '{self.__Currency}', Highscore = '{self.__Highscore}', Red = '{self.__Red}', Green = '{self.__Green}', Blue = '{self.__Blue}' WHERE user_id = '{self.__UserId}'"

        mycursor.execute(sql)

        mydb.commit()

        print(mycursor.rowcount, "record(s) affected")

    def addToDB(self):
        mycursor = mydb.cursor()

        sql = "INSERT INTO users (user_name, password, Phone_number, ingame_currency) VALUES (%s, %s, %s, %s)"
        val = (f"{self.__Name}", f"{self.__Password}", f"{self.__Phone}", "50")
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        print("1 record inserted, ID:", mycursor.lastrowid)
        self.__UserId = mycursor.lastrowid
        print(self.__UserId)




#createUser()

UserList = extractDB()


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([800,600])
background3 = pygame.image.load('Background3.jpg')
base_font = pygame.font.Font(None, 20)
big_font = pygame.font.Font(None, 40)
user_text = ''
passive_text = 'Type your email'
input_rect = pygame.Rect(50,75,140,32)
popUpType = ''
#colour_active = (100,100,100)
#colour_passive = (227,227,227)

#colour = colour_passive

active = False

class TextBox:
    def __init__(self, x,y, w, h, pc, ac, f, am ,m='', pm='',tc=(0,0,0)):
        self.x_pos = x
        self.y_pos = y
        self.width = w
        self.height = h
        self.message = m
        self.passive_message = pm
        self.function = f
        self.colour = pc
        self.active = False
        self.active_colour = ac
        self.passive_colour = pc
        self.above_message = am
        self.text_colour = tc

        self.input_rect = pygame.Rect(x,y,w,h)

    def IsActive(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
                self.colour = self.active_colour
                return True
            else:
                self.active = False
                self.colour = self.passive_colour
                return False

    def ActiveFalse(self):
        global screen
        global base_font
        if not self.active:
            x = base_font.render(self.passive_message, True, (227, 227, 227))
            screen.blit(x, (self.input_rect.x + 5, self.input_rect.y + 8))

    def IsTyping(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.message = self.message[0:-1]#backspace
                elif event.key == pygame.K_RETURN:

                    self.function()#executes function if box is selected and enter is pressed

                else:
                    self.message += event.unicode#to write to the textbox

    def EverythingElseLoop(self):
        global screen
        global base_font
        text = base_font.render(f"{self.above_message}", True, self.text_colour)
        screen.blit(text, (self.input_rect.x, self.input_rect.y - 20))

        pygame.draw.rect(screen, self.colour, self.input_rect, 2)

        text_surface = base_font.render(self.message, True, self.text_colour)
        screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        if text_surface.get_width() >= self.input_rect.w:
            self.input_rect.w = text_surface.get_width() + 20

    def GetMessage(self):
        return self.message

    def SetMessage(self, msg):
        self.message = msg


def display():
    print(username.GetMessage())


def popUp(msg, colour, screen):
    pygame.draw.rect(screen, colour, pygame.Rect(0, 0, 800, 40))
    y = len(msg) * 6#so that no matter on the message length it is always in the middle
    x = big_font.render(str(msg), True, (240, 240, 240))
    screen.blit(x, (400-y, 8))


def button(msg, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(click)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, (0,255,0), (x, y, w, h))
        if click[0] == 1 and action != None:
            action()


    else:
        pygame.draw.rect(screen, (0,200,0), (x, y, w, h))


    displayX(f"{msg}", (x + (w / 2)), (y + (h / 2)))



def CheckCodeAndPass():
    global code
    global  currentUser
    global even
    global popUpType
    if 'code' in globals():
        try:
            guess = int(newCode.GetMessage())
        except:
            guess = newCode.GetMessage()
        if code == guess:
            if len(newPassword.GetMessage()) >= 5:
                userNameGuess = username.GetMessage()

                for i in UserList:
                    if i.GetName() == userNameGuess:
                        XORpassword = XORcipher(newPassword.GetMessage())
                        i.SetPassword(XORpassword)
                        currentUser = i
                        even = 0
                        popUpType = 'success'
            else:
                even = 0
                popUpType = 'Weak Password'
        else:
            even = 0
            popUpType = 'Code Incorrect'



username = TextBox(50,125,180,32,(227,227,227), (100,100,100), display, 'Enter your username:')
password = TextBox(50,200,180,32,(227,227,227), (100,100,100), login, 'Enter your password:')
newPassword = TextBox(300,200,180,32,(227,227,227), (100,100,100), CheckCodeAndPass, 'Enter your new password:')
newCode = TextBox(300,125,180,32,(227,227,227), (100,100,100), display, 'Enter The Code:')
Reset = False

def firstScreen():
    global currentUser
    global even
    global popUpType



    #even = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not Reset:
                username.IsActive(event)
                username.IsTyping(event)

                password.IsActive(event)
                password.IsTyping(event)

            if Reset:
                newPassword.IsActive(event)
                newPassword.IsTyping(event)
                newCode.IsActive(event)
                newCode.IsTyping(event)
        screen.fill((255,255,255))
        screen.blit(background3, [0, 0])
        if not Reset:
            username.ActiveFalse()
            username.EverythingElseLoop()
            password.ActiveFalse()
            password.EverythingElseLoop()

            button("Log in", 325, 375, 100, 50, login)
        button("Create User", 300, 450, 150, 50, createUserPage)

        if Reset:


            newPassword.ActiveFalse()
            newPassword.EverythingElseLoop()
            newCode.ActiveFalse()
            newCode.EverythingElseLoop()

            button('Confirm', 325, 375, 100, 50, CheckCodeAndPass)
            if even <= 500:
                popUp('Code Sent', (21, 235, 14), screen)




        if 'even' in globals():
            even +=1

            if even<= 500 and popUpType == 'success':
                popUp('LOGGED IN', (26, 199, 4), screen)

                if even == 100:
                    #print(currentUser.GetName())
                    setUser(currentUser)
                    game_intro()
                    print('yes')
                    #username.SetMessage('')
                    #password.SetMessage('')
            if even<= 500 and popUpType =='Weak Password':
                popUp('Password too short', (235, 21, 14), screen)
                button('Forgot Password', 275, 525, 200, 50, ResetPass)

            if even<= 500 and popUpType == 'Code Incorrect':
                popUp('Code Wrong', (235, 21, 14), screen)
                button('Forgot Password', 275, 525, 200, 50, ResetPass)

            elif popUpType =='PasswordIncorrect':

                button('Forgot Password', 275, 525, 200, 50, ResetPass)

                if even <= 300:

                    popUp('Password Incorrect', (235, 21, 14), screen)

                    if even == 1:
                        password.SetMessage('')
            elif even <= 500 and popUpType == 'UsernameIncorrect':
                popUp('Username Incorrect', (235, 21, 14), screen)
                if even == 1:
                    username.SetMessage('')
                    password.SetMessage('')




        pygame.display.flip()
        clock.tick(60)



def ResetPass():
    global Reset
    global even
    even = 0
    userNameGuess = username.GetMessage()
    Reset = True
    for i in UserList:
        if i.GetName() == userNameGuess:
            phone = i.GetPhone()
    SendSMS(phone)




choose_username = TextBox(300,150,180,32,(227,227,227), (100,100,100), display, 'Choose a username:')
choose_password = TextBox(300,225,180,32,(227,227,227), (100,100,100), MakeUser, 'Choose a password:')
choose_phone = TextBox(300,300,180,32,(227,227,227), (100,100,100), MakeUser, 'Enter your phone:')
code_guess = TextBox(300,375,180,32,(227,227,227), (100,100,100), MakeUser, 'Enter code:')
firstScreen()




