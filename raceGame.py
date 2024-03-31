import pygame
import time
import random
import mysql.connector
from time import sleep
from mysql.connector import errorcode
from tkinter import *
from tkinter import colorchooser
import matplotlib.pyplot as plt


from binance_futures import *



mydb = mysql.connector.connect(
  host="77.68.35.85",
  user="y13felix",
  password="x6J5de_13",
  database="y13felix"

)



pygame.init()



display_width = 800
display_height = 600






UserColour = None



car_width = 64


pause = False


sens = 10

data2 = []


screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Felix's racecar game")
clock = pygame.time.Clock()

policeMotorbike = pygame.image.load('motorbike.png')
car1 = pygame.image.load('racecar.png')
car2 = pygame.image.load('racing.png')
car3 = pygame.image.load('racef1.png')
icon = pygame.image.load('pygame_icon.png')
bnbPic = pygame.image.load('bnb.png')
xmrPic = pygame.image.load('monero.png')
ethPic = pygame.image.load('ethereum.png')
btcPic = pygame.image.load('bitcoin.png')
coinIcon = pygame.image.load('coin.png')
background2 = pygame.image.load('pygame intro screen.png')
CryptoBackground = pygame.image.load('CryptoBackground.jpg')
pygame.display.set_icon(icon)


carImg = None
background = pygame.image.load('road.png')

carSelect = True


def displayX(number, x, y,textbefore="", size=25, c='y'):#c for center
    font = pygame.font.SysFont(None, size)

    text1 = font.render(textbefore +str(number), True, (0,0,0))
    if c == 'y':
        text = text1.get_rect()
        text.center = (x,y)

        screen.blit(text1, text)#if the text should be in the center
    else:
        screen.blit(text1, (x,y))# if it should start at the specified x and y






def quit_car():
    global carSelect
    carSelect = False






instructionQueue = []
instructionQueue2 =[]
pointer = 0
class engine:
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y

    def GetX(self):
        return self.x
    def GetY(self):
        return  self.y
    def displayCar(self):
        screen.blit(self.img, (self.x, self.y))

    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y




class cars(engine):
    def __init__(self,n,img, x,y,w):
        super().__init__(img=img, x=x, y=y)

        self.name = n
        #self.img = img
        #self.x = x
        #self.y = y
        self.width = w
        self.owned = self.CheckOwned()
        self.dodged = 0
        i = self.CheckCost()
        self.cost = i[2]
        self.EffectScore = i[0]
        self.EffectCoins = i[1]
        self.id = i[3]

    def ChangeX(self, x):
        self.x += x
    def ChangeY(self,y):

        self.y +=y
    def ChangeDodged(self):
        self.dodged += 1
    def SetDodged(self,n):
        self.dodged = n

    def GetDodged(self):
        return self.dodged


    def GetWidth(self):
        return self.width



    def GetScoreMulti(self):
        return self.EffectScore
    def GetCoinsMulti(self):
        return self.EffectCoins

    def CheckCost(self):
        sql = f"SELECT EffectScore, EffectCoins, Cost, Car_ID FROM Cars WHERE Name = '{self.name}';"
        mycursor = mydb.cursor()
        mycursor.execute(sql)

        myresult = mycursor.fetchone()
        return myresult

    def CheckOwned(self):
        sql = f"SELECT Quantity FROM users2Cars INNER JOIN Cars ON users2Cars.Car_ID = Cars.Car_ID WHERE users2Cars.user_id = '{user.GetID()}' AND Cars.Name = '{self.name}';"
        mycursor = mydb.cursor()
        mycursor.execute(sql)

        myresult = mycursor.fetchone()
        try:
            owned = myresult[0]
            if owned == 1:
                return True
            return False
        except:
            return False

    def displayCar(self):
        screen.blit(self.img, (self.x, self.y))


    def display(self):
        screen.blit(self.img, (self.x, self.y))
        font = pygame.font.Font(None, 20)
        text = font.render(f"Score Multiplier: {str(self.EffectScore)}", True, (0,0,0))
        screen.blit(text, ((self.x - 20), (self.y - 15)))
        text = font.render(f"Coins Multiplier: {str(self.EffectCoins)}", True, (0,0,0))
        screen.blit(text, ((self.x-20), (self.y - 30)))
        if self.owned:
            button("Select", self.x-20, self.y +80, 100, 50, self.select)

        elif self.owned == False:
            button(f"Buy: {self.cost}", self.x - 20, self.y + 80, 100, 50, self.buy)
    def select(self):
        global carImg
        carImg = self#change to pass self here


    def GetImg(self):
        return self.img

    def GetOwned(self):
        return self.owned

    def buy(self):
        if user.GetCurrency() >= self.cost:
            currency = user.GetCurrency()-self.cost
            user.setCurrency(currency)
            mycursor = mydb.cursor()
            sql = f"INSERT INTO users2Cars (user_id, Car_ID, Quantity) VALUES ('{user.GetID()}','{self.id}',1)"
            mycursor.execute(sql)

            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")
            self.owned = True
            self.select()

        else:

            pass





class Obstacles(engine):
    def __init__(self, s, sp, e, x, y,w):
        super().__init__(img=s, x=x, y=y)
        #self.sprite = s
        self.speed = sp
        self.effect = e

        self.width = w



    def getSpeed(self):
        return self.speed
    def setSpeed(self,n):
        self.speed = n



    def CheckIfOff(self):
        if self.y > display_height:
            self.y = -100
            self.x = random.randrange(0, display_width)


    def contactWithPlayer(self, player):
        if player.GetY() < self.y + 64 and player.GetY()+64> self.y:

            if player.GetX() > self.x and player.GetX() < self.x + self.width or player.GetX() + player.GetWidth() > self.x and player.GetX() + player.GetWidth() < self.x + self.width:

                eval(self.effect+'()')








class Coins():
    def __init__(self, i,n, p,img,x,y,ot,q):
        self.__ID = i
        self.__Name =n
        self.__Price = p
        self.__img = img
        self.x = x
        self.y = y
        self.orderType = ot
        self.__queue = q
        self.__Amount = self.GetQuantity()

    def getID(self):
        return self.__ID

    def getName(self):
        return self.__Name
    def getPrice(self):
        return self.__Price
    def CoinButton(self,msg,x,y,w,h,ic,ac,action=None,paramaters=None):
        #same as button but with ability to pass th name of the coin through to the queue
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None and paramaters != None:
                if int(self.__Amount) >0:
                    self.__Amount = int(self.__Amount) -1
                    action(paramaters)
                else:
                    pass
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))

        displayX(f"{msg}", (x + (w / 2)), (y + (h / 2)), size=15)


    def displayCoin(self):

        screen.blit(self.__img, (self.x, self.y))

    def GetQuantity(self):
        sql = f"SELECT Quantity FROM Coins2Users INNER JOIN Coins ON Coins2Users.Coin_ID = Coins.Coin_ID WHERE Coins2Users.user_id = '{user.GetID()}' AND Coins.Symbol = '{self.__Name+'USDT'}';"
        mycursor = mydb.cursor()
        mycursor.execute(sql)

        myresult = mycursor.fetchone()
        try:
            currency = myresult[0]
            currency = str(currency)
        except:
            currency = 0
            currency = str(currency)
        return currency
    def AddQuantity(self,x):
        self.__Amount = int(self.__Amount)+x
    def EverythingElseLoop(self):

        if self.orderType == 'buy':
            self.displayCoin()
            self.__Amount= 1000000

            font = pygame.font.Font(None, 20)
            text = font.render(str(self.__Price), True, (0,0,0))
            screen.blit(text, ((self.x+25), (self.y-15)))
            self.CoinButton(('Buy '+ self.__Name),(self.x+7),(self.y+70), 50, 30,(0,200,0), (0,255,0), self.__queue.addToQueue,self)
        elif self.orderType =='sell':
            self.displayCoin()
            font = pygame.font.Font(None, 20)
            text = font.render(f"{str(self.__Amount)}:{str(self.__Price)}", True, (0,0,0))
            screen.blit(text, ((self.x + 20), (self.y - 15)))
            self.CoinButton(('Sell ' + self.__Name), (self.x + 7), (self.y + 70), 50, 30, (0, 200, 0), (0, 255, 0), self.__queue.addToQueue, self)



def RawPrice(symbol):
    secret = 'feee327df4dc662e369b5822229b8c64024ac022530aaea219d2ee23da09ba44'
    public = 'a2afdb8290714eac935465c10f03cb1742a263cb4c1b847eb5cb6d59f39caacf'
    binance = BinanceFutures(public, secret)
    info = binance.getPrice(symbol)
    price = info['price']
    price = float(price)
    return price

def CalculatePrice(symbol):
    price = RawPrice(symbol)

    exchaneRate = 50
    ingamePrice = int(price / exchaneRate) + 1
    return ingamePrice

    #exhange rate of 100
    #create new instance of the class coins each time it is page is entered


class CoinQueue():
    def __init__(self, a, t):
        self.__queue = a
        self.__Type = t

    def getQueue(self):
        return self.__queue

    def getQueueAsString(self):
        x = ''
        for i in self.__queue:
            try:
                x += i.getName() + ", "
            except:
                x +=i + ", "
        return x

    def addToQueue(self,x):
        sleep(1)
        self.__queue.append(x) # This is where aggregation would occur

    def clearQueue(self):
        x = self.__queue
        self.__queue = []
        for i in x:
            i.AddQuantity(1)
        return x
    def displayQueue(self, x, y):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Queue: " + self.getQueueAsString(), True, (0,0,0))
        screen.blit(text, (x, y))

    def executeQueue(self):


        if self.__Type == 'buy':
            if user.GetCurrency() < self.sumOfQueue() and self.__queue != []:
                pass
            elif self.__queue == []:
                pass
            else:
                sqlList = list(map(self.createSQL,self.__queue))


                user.setCurrency(user.GetCurrency() - self.sumOfQueue())


                #in order to add however many of each coin in queue to the list

                self.__queue = []

                sleep(1)
        elif self.__Type == 'sell':
            sqlList = list(map(self.SellSQL, self.__queue))

            user.setCurrency(user.GetCurrency() + self.sumOfQueue())

            self.__queue = []

            sleep(1)


    def SellSQL(self, coin):
        mycursor = mydb.cursor()
        sql = f"INSERT INTO Orders (user_id, Coin_ID, ingame_price,order_date, actual_Price, BuyORSell) VALUES ('{user.GetID()}','{coin.getID()}','{coin.getPrice()}','{self.GetDateTime()}', '{RawPrice(coin.getName() + 'USDT')}', 'sell')"
        mycursor.execute(sql)

        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

        sql = f"UPDATE Coins2Users SET Quantity = Quantity-1 WHERE user_id = '{user.GetID()}' AND Coin_ID = '{coin.getID()}'"
        mycursor.execute(sql)

        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
        return sql

    def createSQL(self, coin):

        mycursor = mydb.cursor()
        sql = f"INSERT INTO Orders (user_id, Coin_ID, ingame_price,order_date, actual_Price, BuyORSell) VALUES ('{user.GetID()}','{coin.getID()}','{coin.getPrice()}','{self.GetDateTime()}', '{RawPrice(coin.getName()+'USDT')}','buy')"
        mycursor.execute(sql)

        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

        sql = f"UPDATE Coins2Users SET Quantity = Quantity+1 WHERE user_id = '{user.GetID()}' AND Coin_ID = '{coin.getID()}'"
        mycursor.execute(sql)

        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

        if mycursor.rowcount == 0:
            sql = f"INSERT INTO Coins2Users (user_id, Coin_ID, Quantity) VALUES ('{user.GetID()}','{coin.getID()}',1)"
            mycursor.execute(sql)

            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")

        return sql

    def GetDateTime(self):
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
        return dt_string

    def sumOfQueue(self):
        prices = list(map(lambda x :x.getPrice(), self.__queue))
        total = sum(prices)
        return total

    #all the functionality for storing and buying the coins

sellCoins = True
def QuitSell():
    global sellCoins
    sellCoins = False
def sell_coins():
    global sellCoins

    sellCoins = True
    #print(user)
    coinQueue = CoinQueue([], 'sell')
    bnb = Coins(3, 'BNB', CalculatePrice('BNBUSDT'), bnbPic, 225, 300, 'sell', coinQueue)#composition as the queue attribute of coins is a coinQueue
    xmr = Coins(4, 'XMR', CalculatePrice('XMRUSDT'), xmrPic, 425, 300, 'sell', coinQueue)
    btc = Coins(1, 'BTC', CalculatePrice('BTCUSDT'), btcPic, 325, 300, 'sell', coinQueue)
    eth = Coins(2, 'ETH', CalculatePrice('ETHUSDT'), ethPic, 525, 300, 'sell', coinQueue)

    while sellCoins:

        listOfCurrentEvents = pygame.event.get()
        listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
        QuitList = list(filter(lambda x: x == pygame.QUIT, listOfEvents))
        if len(QuitList) > 0:
            pygame.quit()
            quit()



        screen.fill((255,255,255))
        displayX(user.GetCurrency(), 0, 0, "Balance: ", c='n')
        coinQueue.displayQueue(0, 20)
        bnb.EverythingElseLoop()
        xmr.EverythingElseLoop()
        btc.EverythingElseLoop()
        eth.EverythingElseLoop()


        displayX("Coins", (display_width / 2), (display_height / 4), size=70)


        button("Clear Queue", 550, 500, 150, 50, coinQueue.clearQueue)
        button("Continue", 350, 500, 100, 50, QuitSell)
        button("Execute", 150, 500, 100, 50, coinQueue.executeQueue)


        pygame.display.update()
        clock.tick(60)




viewCoins = True
def quit_coins():
    global viewCoins
    viewCoins = False

shop = True
def quit_shop():
    global shop
    shop = False
def coin_shop():
    global shop
    shop = True
    while shop:
        listOfCurrentEvents = pygame.event.get()
        listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
        QuitList = list(filter(lambda x: x == pygame.QUIT, listOfEvents))
        if len(QuitList) > 0:
            pygame.quit()
            quit()

        screen.fill((255,255,255))
        screen.blit(CryptoBackground, [0, 0])

        displayX("Coin Shop", (display_width/2),(display_height/2), size=100)

        button("Back",100, 100, 100, 50, quit_shop)
        button("SELL", 300, 100, 100, 50, sell_coins)
        button("Portfolio", 450, 100, 100, 50, portfolio)
        button("BUY", 600, 100, 100, 50, buy_coins)

        pygame.display.update()
        clock.tick(15)

Portfolio = False
def QuitPortfolio():
    global Portfolio
    Portfolio = False
view = 'real'
def SwitchView():
    global view
    if view == 'real':
        view = 'game'
    else:
        view = 'real'
    sleep(1)
def portfolio():
    global Portfolio
    global view
    Portfolio = True

    view = 'real'
    XMRGraph = Graphs(300, 330,"XMR")
    BTCGraph = Graphs(300, 210, "BTC")
    ETHGraph = Graphs(300, 270, "ETH")
    BNBGraph = Graphs(300, 150,"BNB")


    while Portfolio:
        listOfCurrentEvents = pygame.event.get()
        listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
        QuitList = list(filter(lambda x: x == pygame.QUIT, listOfEvents))
        if len(QuitList) > 0:
            pygame.quit()
            quit()
        screen.fill((255,255,255))


        displayX("Portfolio", (display_width / 2), (display_height -100), size=60)

        button("Back", 100, 500, 100, 50, QuitPortfolio)
        if view == 'real':
            button("Game", 100, 50, 100, 50, SwitchView)
        else:
            button("Real", 100, 50, 100, 50, SwitchView)
        XMRGraph.alwaysLoop(view)
        BTCGraph.alwaysLoop(view)
        BNBGraph.alwaysLoop(view)
        ETHGraph.alwaysLoop(view)

        button("Total Table", 300, 90, 200, 50, PortfolioTable)


        pygame.display.update()
        clock.tick(15)
class Graphs:
    def __init__(self,x,y,s):
        self.x = x
        self.y = y
        self.symbol = s
        self.view = 'real'

    def alwaysLoop(self, v):
        button((self.symbol + " Graph"), self.x, self.y, 200, 50, self.retriveMin)
        if self.view != v:
            self.view = v

    def retriveMin(self):
        sleep(1)
        sql = f"SELECT Quantity FROM Coins2Users INNER JOIN Coins ON Coins2Users.Coin_ID = Coins.Coin_ID WHERE Coins2Users.user_id = '{user.GetID()}' AND Coins.Symbol = '{self.symbol + 'USDT'}';"
        mycursor = mydb.cursor()
        mycursor.execute(sql)

        myresult = mycursor.fetchone()
        if myresult:
            currency = myresult[0]
            if currency > 0:
                sql = f"SELECT order_date, ingame_price FROM Orders JOIN Coins ON Orders.Coin_ID = Coins.Coin_ID WHERE BuyORSell ='buy' and Coins.Symbol = '{self.symbol+'USDT'}' and user_id = {user.GetID()} ORDER BY order_date DESC LIMIT 1 OFFSET {currency-1};"#in order to get the graph from when they first bought
                mycursor = mydb.cursor()
                mycursor.execute(sql)

                myresult = mycursor.fetchone()
                self.CreateGraph(myresult)
            else:
                pass

        else:
            currency = 0
            pass

    def CreateGraph(self, m):
        secret = 'feee327df4dc662e369b5822229b8c64024ac022530aaea219d2ee23da09ba44'
        public = 'a2afdb8290714eac935465c10f03cb1742a263cb4c1b847eb5cb6d59f39caacf'
        binance = BinanceFutures(public, secret)

        x = binance.get_candles(f'{self.symbol}USDT', '1h')


        date_list = list(filter(lambda x: x[0] >= m[0], x))#keeps dates only that are newer than when the client first bought the coin m[0] being that date




        dates = []
        prices = []
        for i in date_list:
            dates.append(i[0])
            prices.append(i[1])
        #print(self.view)
        if self.view == 'game':
            prices = list(map(lambda x: x / 50 + 1,prices))





        fig = plt.figure(figsize=(800 / 96, 600 / 96), dpi=96)


        plt.plot(dates, prices)


        plt.xlabel("Date")
        plt.xticks(rotation=45)


        plt.ylabel("Price")
        plt.title(f'{self.symbol} Price History')


        plt.show()


def CreateTableSQL():
    mycursor = mydb.cursor()
    sql = f"SELECT Coin_ID, Quantity FROM Coins2Users WHERE user_id = '{user.GetID()}';"
    mycursor.execute(sql)


    myresult = mycursor.fetchall()


    x = []
    for i in myresult: # sum of price of coins when originally bought which they still own
        x.append(f"SELECT Coins.Symbol, SUM(ingame_price) FROM (SELECT * FROM Orders WHERE Orders.user_id = {user.GetID()} and Orders.BuyORSell ='buy' and Orders.Coin_ID = {i[0]} Order BY order_date DESC LIMIT {i[1]} ) AS Recent INNER JOIN Coins ON Recent.Coin_ID = Coins.Coin_ID")
    y = ' UNION ALL '.join(x)#creates a list of sql statements which will be executed at the same time using union al

    return y




def CalculateProfitLoss(values):

    old = int(values[1])
    new = int(values[2])
    profit = (new-old)/old *100
    profit = round(profit, 2)
    if profit > 0:
        profit = "+"+str(profit)
    elif profit<0:
        profit = str(profit)


    values.append(profit)

    return values


def PortfolioTable():




    sql = CreateTableSQL()
    if sql != "":
        mycursor = mydb.cursor()
        mycursor.execute(sql)

        myresult = mycursor.fetchall()

        x = []
        table = []
        bnb = Coins(3, 'BNB', CalculatePrice('BNBUSDT'), bnbPic, 225, 300, 'sell', x)
        xmr = Coins(4, 'XMR', CalculatePrice('XMRUSDT'), xmrPic, 425, 300, 'sell', x)
        btc = Coins(1, 'BTC', CalculatePrice('BTCUSDT'), btcPic, 325, 300, 'sell', x)
        eth = Coins(2, 'ETH', CalculatePrice('ETHUSDT'), ethPic, 525, 300, 'sell', x)
        y = [bnb, xmr, btc, eth]
        for i in y:
            for j in myresult:
                if i.getName()+"USDT" == j[0]:
                    j = list(j)
                    j.append(int(i.GetQuantity()) * int(i.getPrice()))
                    print(j)
                    table.append(j) #this code calculates what the total value of the coins is worth now and adds it to table







        list(map(CalculateProfitLoss, table))

        oldTotal = 0
        newTotal = 0
        for i in table:
            oldTotal += int(i[1])
            newTotal += int(i[2])

        TotalPercent = (newTotal-oldTotal)/oldTotal *100
        TotalPercent = round(TotalPercent,2)
        if TotalPercent > 0:
            TotalPercent = "+" + str(TotalPercent)
        elif TotalPercent < 0:
            TotalPercent =  str(TotalPercent)

        table.append(("Total", oldTotal, newTotal,TotalPercent))
        table.insert(0, ("Symbol", "Bought For","Now Worth","Profit/Loss"))


        print(table)













        root = Tk()
        t = Table(root, table)
        root.mainloop()
    else:
        pass

def buy_coins():
    global viewCoins

    viewCoins = True
    print(user)
    coinQueue = CoinQueue([], 'buy')
    bnb = Coins(3,'BNB', CalculatePrice('BNBUSDT'), bnbPic, 225, 300, 'buy',coinQueue)
    xmr = Coins(4,'XMR', CalculatePrice('XMRUSDT'), xmrPic, 425, 300, 'buy',coinQueue)
    btc = Coins(1,'BTC', CalculatePrice('BTCUSDT'), btcPic, 325, 300, 'buy',coinQueue)
    eth = Coins(2,'ETH', CalculatePrice('ETHUSDT'), ethPic, 525, 300, 'buy',coinQueue)

    while viewCoins:
        listOfCurrentEvents = pygame.event.get()
        listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
        QuitList = list(filter(lambda x: x == pygame.QUIT, listOfEvents))
        if len(QuitList) > 0:
            pygame.quit()
            quit()





        screen.fill((255,255,255))
        displayX(user.GetCurrency(),0,0,"Balance: ", c='n')
        coinQueue.displayQueue(0,20)
        bnb.EverythingElseLoop()
        xmr.EverythingElseLoop()
        btc.EverythingElseLoop()
        eth.EverythingElseLoop()



        displayX("Coins", (display_width / 2), (display_height / 4), size=70)


        button("Clear Queue", 550, 500, 150, 50, coinQueue.clearQueue)
        button("Continue", 350, 500, 100, 50, quit_coins)
        button("Execute", 150, 500, 100, 50, coinQueue.executeQueue)


        pygame.display.update()
        clock.tick(60)

    #view coins screen

#the user can now select a car


def car_select():
    global carSelect

    Car1 = cars('Racer',car1, 170, 375, 64)
    Car2 = cars('Drag', car2, 570, 380, 64)
    Car3 = cars('Formula1', car3, 370, 270, 64)

    carSelect = True 
    while carSelect == True:
        listOfCurrentEvents = pygame.event.get()
        listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
        QuitList = list(filter(lambda x: x == pygame.QUIT, listOfEvents))
        if len(QuitList) > 0:
            pygame.quit()
            quit()

        screen.fill((255,255,255))

        Car1.display()
        Car2.display()
        Car3.display()

        displayX("Cars",(display_width/2),(display_height/4), size=100)

        displayX(user.GetCurrency(), 0, 0, "Balance: ", c='n')
        

        button("Continue",350,500,100,50,quit_car)

        pygame.display.update()
        clock.tick(60)
def crash():
    score = carImg.GetDodged()*carImg.GetScoreMulti()

    highscore = user.GetHighscore()
    user.setCurrency(user.GetCurrency())
    #print(highscore)

    if score >= highscore:
        user.SetHighscore(score)

        displayX("New Highscore!",(display_width/2),(display_height/2), size=100 )
        while True:
            listOfCurrentEvents = pygame.event.get()
            listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
            QuitList = list(filter(lambda x: x == pygame.QUIT, listOfEvents))
            if len(QuitList) > 0:
                pygame.quit()
                quit()


            button("Play again",150,450,110,50,game_loop)
            button("Main Menu", 350, 450, 110, 50, game_intro)
            button("Quit",550,450,100,50,quitgame)
            

            
            pygame.display.update()
            clock.tick(15)
    else:


        displayX("You Crashed",(display_width/2),(display_height/2), size=100 )
        while True:
            listOfCurrentEvents = pygame.event.get()
            listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
            QuitList = list(filter(lambda x: x == pygame.QUIT, listOfEvents))
            if len(QuitList) > 0:
                pygame.quit()
                quit()

            button("Play again", 150, 450, 110, 50, game_loop)
            button("Main Menu", 350, 450, 110, 50, game_intro)
            button("Quit", 550, 450, 100, 50, quitgame)
            

            
            pygame.display.update()
            clock.tick(15)



def button(msg,x,y,w,h,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    active = (min(UserColour[0] + 10, 255), min(UserColour[1] + 10, 255), min(UserColour[2] + 30, 255))
#this is the coulour that the button would be when the user hovers over it, adds 10 so that it looks brighter but with a max of 255

        
    if x+w >mouse[0] > x and y+h > mouse[1] >y:
        pygame.draw.rect(screen, active, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
            

    else:
        pygame.draw.rect(screen, UserColour, (x,y,w,h))



    displayX(f"{msg}", (x+(w/2)), (y+(h/2)))


class Table:

    def __init__(self, root, val, w=0):
        self.rows = len(val)
        self.columns = len(val[0])
        self.values = val
        self.width = w
        self.root = root

        if self.width == 0:
            self.width = self.columns*5

        for i in range(self.rows):
            for j in range(self.columns):
                if i == 0:
                    self.entry = Label(self.root, width=self.width, fg='black', text=self.values[i][j],
                                       font=('Ariel', 16, 'bold'), relief='ridge') #first row would be black the rest blue

                    self.entry.grid(row=i, column=j)
                else:
                    self.entry = Label(self.root, width=self.width, fg='blue', text=self.values[i][j],
                                       font=('Ariel', 16, 'bold'), relief='ridge')

                    self.entry.grid(row=i, column=j)

def highscores():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT user_name, Highscore FROM users ORDER BY Highscore DESC LIMIT 5;")

    myresult = mycursor.fetchall()

    table = [("POS.", "NAME", "SCORE")]
    for i, row in enumerate(myresult):  # keep track of the number of iterations (loops) in a loop
        table.append([i + 1] + list(row))

    root = Tk()
    t = Table(root, table)
    root.mainloop()


def game_intro():
    intro = True
    global carImg
    global UserColour

    Car1 = cars('Racer', car1, 170, 375, 64)
    Car2 = cars('Drag', car2, 570, 380, 64)
    Car3 = cars('Formula1', car3, 370, 270, 64)
    #use filter to only get the ones which are owned and then use random to randomly select one
    UserColour = user.GetColour()

    x = [Car1, Car3, Car2]

    y = []
    y = list(filter(lambda i: i.CheckOwned(),x))
    print(y)



    if y !=[]:
        carImg = random.choice(y)
        print(carImg)



    print(carImg)

    while intro:

        listOfCurrentEvents = pygame.event.get()
        listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
        QuitList = list(filter(lambda x: x == pygame.QUIT, listOfEvents))
        if len(QuitList) > 0:
            pygame.quit()
            quit()

        screen.fill((255,255,255))
        screen.blit(background2, [0, 0])


        button("GO",150,450,100,50,game_loop)
        button("QUIT",550,450,100,50,quitgame)
        button("CAR",350,450,100,50,car_select)
        button("HIGHSCORES", 350, 300, 150, 50, highscores)
        button("COINS", 550, 300,100,50, coin_shop)
        button("Colours", 550, 200, 100, 50, ColoursScheme)
        if carImg is None:
            popUp("Please buy a car first", UserColour, screen)

        
        pygame.display.update()
        clock.tick(15)

big_font = pygame.font.Font(None, 40)
def popUp(msg, colour,screen):
    pygame.draw.rect(screen, colour, pygame.Rect(0, 0, 800, 40))
    y = len(msg) * 6#so that no matter on the message length it is always in the middle
    x = big_font.render(str(msg), True, (240, 240, 240))
    screen.blit(x, (400-y, 8))

def ColoursScheme():
    global UserColour


    mycolour = colorchooser.askcolor()
    if mycolour[0] is not None:
        print(mycolour[0])
        print(mycolour[0][1])
        user.SetColour(mycolour[0])
        UserColour = mycolour[0]


def quitgame():
    pygame.quit()
    quit()

def setUser(newUser):
    global user
    user = newUser

OBCoin = Obstacles(coinIcon, 10, 'CoinEffect', random.randrange(0, display_width), -300, 64 )
def CoinEffect():
    global OBCoin
    OBCoin.setY(-100)
    OBCoin.setX(random.randrange(0, display_width))
    user.tempSetCurrency(user.GetCurrency()+1*carImg.GetCoinsMulti())


def game_loop():
    global OBCoin

    global carImg

    global sens
    if carImg is not None:



        mph = 0
        time = 0
        clock = pygame.time.Clock()



        x_change = 0
        y_change = 0

        OB1 = Obstacles(policeMotorbike, 10, 'crash', random.randrange(0, display_width), -600, 64)
        OB2 = Obstacles(policeMotorbike, 15, 'crash', random.randrange(0, display_width), -300, 64)
        OBCoin = Obstacles(coinIcon, 10, 'CoinEffect', random.randrange(0, display_width), -300, 64)


        carImg.SetDodged(0)

        carImg.setX(400)
        carImg.setY(500)

        gameExit = False#so that the display keeps on updating until the

        while not gameExit:
            try:
# when my client tested the game he thought the wads keys were used for movement and the game crashed so a try and except statement is necessary.

                listOfCurrentEvents = pygame.event.get()
                listOfEvents = list(map(lambda x: x.type, listOfCurrentEvents))
                QuitList = list(filter(lambda x: x==pygame.QUIT, listOfEvents))
                if len(QuitList)>0:
                    pygame.quit()
                    quit()
                keydownList = list(filter(lambda x: x==pygame.KEYDOWN, listOfEvents))
                if len(keydownList)>0:
                    LeftList = list(filter(lambda x: x.key == pygame.K_LEFT, listOfCurrentEvents))
                    if len(LeftList) > 0:
                        x_change = -sens#global variable of how quick the car should move.
                    RightList = list(filter(lambda x: x.key == pygame.K_RIGHT, listOfCurrentEvents))
                    if len(RightList) > 0:
                        x_change = sens
                    UpList = list(filter(lambda x: x.key == pygame.K_UP, listOfCurrentEvents))
                    if len(UpList) >0:
                        y_change = -sens
                keyUpList = list(filter(lambda x: x==pygame.KEYUP, listOfEvents))
                if len(keyUpList) > 0:
                    SidewaysUp = list(filter(lambda x: x.key == pygame.K_LEFT or x.key == pygame.K_RIGHT, listOfCurrentEvents))
                    if len(SidewaysUp) >0:
                        x_change = 0
                    UpKeyUp = list(filter(lambda x: x.key == pygame.K_UP, listOfCurrentEvents))
                    if len(UpKeyUp)>0:
                        y_change = 2
            except:
                pass







            carImg.ChangeX(x_change)
            carImg.ChangeY(y_change)
            screen.fill((255,255,255))
            screen.blit(background, [0, 0])

            if OB1.GetY() > display_height:
                carImg.ChangeDodged()
                OB1.CheckIfOff()

            OB1.displayCar()
            OB1.setY(OB1.GetY()+OB1.getSpeed())# makes the obstacle go down

            OB1.contactWithPlayer(carImg)

            OBCoin.displayCar()
            OBCoin.setY(OBCoin.GetY()+OBCoin.getSpeed())
            OBCoin.contactWithPlayer(carImg)
            OBCoin.CheckIfOff()


            dt = clock.tick()

            time += dt

            if time > 250:#incriments mph
                mph += 1
                time = 0

            carImg.displayCar()

            displayX(carImg.GetDodged()*carImg.GetScoreMulti(),0,0, "Score: ", c='n')
            displayX(mph,0,20, "MPH: ",c='n')
            displayX(user.GetHighscore(), 0, 40, "Highscore: ",c='n')
            displayX(user.GetCurrency(), 0, 60, "Coins: ",c='n')

            if carImg.GetX() > display_width - carImg.GetWidth() or carImg.GetX() < 0:
                crash()# if car hits borders it crashes
            if carImg.GetY() > display_height - carImg.GetWidth() or carImg.GetY() < 0:
                crash()



            if carImg.GetDodged() >= 10:
                OB1.setSpeed(15)
                OBCoin.setSpeed(15)
                OB2.displayCar()
                OB2.setY(OB2.GetY() + OB2.getSpeed())
                OB2.contactWithPlayer(carImg)
                OB2.CheckIfOff()



                #if car.dodged >= 10 OB1 speed = 5 or something like that





            pygame.display.update()
            clock.tick(60)
    else:

        pass









