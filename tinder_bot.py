from selenium import webdriver
import random
from time import sleep
import time
from secrets import username, password, nr
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from gtts import gTTS
from playsound import playsound



def spraak(tekst, naamf):
    language = 'nl'
    speech = gTTS(text = tekst, lang = language, slow = False)
    naamfile = naamf + ".mp3"
    speech.save(naamfile)
    path = "/Users/admin/Documents/Tech_Projects/Python/tinderbot/" + naamfile
    playsound(path)



class TinderBot():
    def __init__(self):
        self.language = 'nl'
        self.driver = webdriver.Chrome()
        self.driver.get("https://tinder.com")
        sleep(3)
        pop = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/div[1]/button")
        pop.click()
        self.nrmatch = 0
        self.nrlike = 0
        self.nrdislike = 0
        sleep(3)
    
    #een countdown timer
    def countdown(self,t):
        print("start timer")
        while(t>=0):
            min, sec = divmod(t, 60)
            clock = '{:02}:{:02}'.format(min,sec)
            print(clock, end='\r')
            sleep(1)
            t -=1
        print("\ntimer done")
    

    #functie om in te loggen op tinder
    def login(self):

        #eerst inloggen via nr
        nrknop = self.driver.find_element_by_xpath("//*[@aria-label = 'Log in with phone number']")
        nrknop.click()
        sleep(2)

        #voer nr in
        nrwindow =  self.driver.find_element_by_xpath("//*[@name = 'phone_number']")   
        nrwindow.send_keys(nr)
        sleep(5)
        
        
        
        #make a separate function of this for try
        try:
            contknop = bot.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/button")
            contknop.click()
            sleep(3)
            #spraak("druk op continue en vul je code in je hebt 40 sec", "beginlog")
            #self.countdown(40)
            cont = self.driver.find_element_by_xpath("//*[@id='modal-manager']/div/div/div/button")
            cont.click()
            spraak("proficiat je bent ingelogd", "login gelukt")
            print('logged in')
            sleep(5)
        except Exception:
            spraak("je hebt 90 sec om zelf in te loggen", "loginfail")
            print("login failed\nje moet nu zelf manueel inloggen je hebt 1 min en 30 sec")
            self.countdown(90)
            
        finally:
            self.hometinder()

        
    def hometinder(self):
        
        spraak("de popups worden vanzelf gesloten, druk nergens op", "popup")
        #allow using location & notifications & deny passport
        loc = self.driver.find_element_by_xpath("//*[@aria-label = 'Allow']")
        loc.click()
        sleep(3)

        notif = self.driver.find_element_by_xpath("//*[@aria-label = 'Enable']")
        notif.click()
        sleep(4)
        try:
            pas = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/button")
            pas.click()
        except Exception:
            print("pasport popup is er niet meer")
        
        spraak("proficiat je bent ingelogd", "ing")


    def like(self, tim):
            right = self.driver.find_element_by_xpath("//*[@aria-label = 'Like']")
            right.click()
            self.nrlike +=1
            sleep(tim)

    def dislike(self):
        left = self.driver.find_element_by_xpath("//*[@aria-label = 'Nope']")
        left.click()
        self.nrdislike += 1
        sleep(0.5)

    def closepopup(self):
        notinter = self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/button[2]")
        notinter.click()
        sleep(0.5)


    def close_match(self, mes = False, msg = 'hola'):
        spraak("proficiat je hebt een match", "match")
        if(mes):
            self.driver.find_element_by_xpath("//*[@id= 'chat-text-area']").send_keys(msg)
        else:
            try:
                self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/main/div[2]/div/div/div[1]/div/div[3]/a").click()
            except Exception:
                try:
                    self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div[3]/a").click()
                except Exception:
                    self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[3]/a").click()
        

        self.nrmatch += 1
        sleep(0.5)
    
    def no_likes_left(self):
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/button[2]").click()
        print("likes zijn op")

    def autoswipe(self, nr, perc, wacht):
        i = 0
        self.nrdislike = 0
        self.nrlike = 0
        self.nrmatch = 0
        while(i<nr):
            try:
                kans = random.random()
                if(kans>(perc/10)):   
                    if(i>2):
                        wacht /= 2
                    self.like(wacht)
                    
                else:  
                    self.dislike()

            except Exception:
                try:
                    self.closepopup()
                except Exception:
                    try:
                        self.close_match()
                    except Exception:
                        self.no_likes_left()
            print(i)
            i+=1
        print("DONE: matches= {} likes= {} dislike= {}".format(self.nrmatch,self.nrlike,self.nrdislike))


bot = TinderBot()


def swipe():
    aantal = int(input("hoeveel wil je swipen?"))
    bot.autoswipe(aantal, 1, 1)
    again = 1
    while(again==1):
        again = int(input("wil je nog eens? (druk 0 of 1)\n"))
        if(again==1):
            aantal = int(input("hoeveel wil je swipen? "))
            bot.autoswipe(aantal, 1, 1)
        
try:
    swipe()
except Exception:
    keuze = int(input("Wat wil je doen? 0 = quit, 1 = autoswipe\n"))
    if(keuze):
        swipe()
